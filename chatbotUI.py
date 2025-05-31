import os
import gradio as gr
from RAG import GT_RAG
from openai import OpenAI
from PyPDF2 import PdfReader
from PIL import Image
import pytesseract
import mimetypes
from RMPInfoGrabber import fetch_professor_data
from GTScheduler import get_enrollment_metadata
from MSCSSpecialization import get_class_requirements
from CanvasIntegration import CanvasAPI
import json

my_rag = GT_RAG('RAG_cache')
openai_key = open('OPENAI_KEY.txt').read().strip()
base_llm = OpenAI(api_key=openai_key)
canvas_api = CanvasAPI(open('CANVAS_KEY.txt').read().strip())

def read_file_content(file_path):
    mime_type, _ = mimetypes.guess_type(file_path)
    content = ""

    if mime_type and mime_type.startswith('text'):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    elif mime_type == 'application/pdf':
        reader = PdfReader(file_path)
        for page in reader.pages:
            content += page.extract_text()
    elif mime_type and mime_type.startswith('image'):
        image = Image.open(file_path)
        content = pytesseract.image_to_string(image)
    else:
        content = f"[Unsupported file type: {mime_type}]"
    return content

def truncate_filename(filename, max_length):
    name, ext = os.path.splitext(filename)
    if len(name) > max_length:
        name = name[:max_length] + '...'
    return f"{name} {ext}"

def build_prompt(rag_input, api_input, user_input, conversation_history, file_content=""):
    prompt = (
        "You will act as Reggie, the Georgia Tech Registration chatbot. "
        "You will be asked a variety of questions about registering for classes at Georgia Tech. "
        "You will keep your answers direct and relevant to the question asked. "
        "If the user asks you a question and you are unsure of the semantics or details of their question, "
        "please ask for clarification until you are confident in answering appropriately. "
        "Avoid providing information that is not relevant to the question asked. "
        "If you are unsure of the answer to a question, please ask for clarification or indicate that you are unsure. "
        "You may be evaluated on the quality of your responses, so please ensure that your responses are clear, concise, and accurate.\n\n"
        f"Conversation History:\n{conversation_history}\n"
        f"Answer the following question to the best of your ability:\n{user_input}\n"
        f"Utilize the following information from live Georgia Tech API's:\n{api_input}\n"
        f"Utilize the following information from Georgia Tech's FAQ documents. Be wary for noisy input:\n{rag_input}\n"
    )
    # Include the file content if available
    if file_content:
        prompt += f"\nAdditional information provided by the user:\n{file_content}\n"
    return prompt

def query_llm(llm, query):
    chat_completion = llm.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": query,
            }
        ],
        model="gpt-3.5-turbo",
    )
    return chat_completion.choices[0].message.content

def build_display_history(history):
    # Build display history, skipping 'file' role messages
    display_history = []
    i = 0
    while i < len(history):
        if history[i]["role"] == "user":
            user_message = history[i]["content"]
            # Check for the corresponding bot response
            bot_message = ""
            if i + 1 < len(history) and history[i + 1]["role"] == "bot":
                bot_message = history[i + 1]["content"]
                i += 1  # Skip the bot message in the next iteration
            display_history.append((user_message, bot_message))
        elif history[i]["role"] == "bot" and (i == 0 or history[i - 1]["role"] != "user"):
            # For the initial bot message or standalone bot messages
            display_history.append((None, history[i]["content"]))
        # Skip messages with role 'file'
        i += 1
    return display_history

def query_function_calls(llm, query):
    # Define the function schema for OpenAI function calling
    function_definitions = [
        {
            "name": "fetch_professor_data",
            "description": "Fetches professor data from RateMyProfessor",
            "parameters": {
                "type": "object",
                "properties": {
                    "professor_name": {
                        "type": "string",
                        "description": "Full name of the professor (e.g., 'John Smith')",
                    }
                },
                "required": ["professor_name"],
            },
        },
        {
            "name": "get_enrollment_metadata",
            "description": "Gets course registration data (such as waitlist and current people registered) from Georgia Tech's Registration Website based off of Course Registration Number (CRN)",
            "parameters": {
                "type": "object",
                "properties": {
                    "course_registration_number": {
                        "type": "string",
                        "description": "Course Registration Number (e.g., 234873)",
                    }
                },
                "required": ["course_registration_number"],
            },
        },
        {
            "name": "get_class_requirements",
            "description": "Gets course requirements from Georgia Tech's official website given a Masters' student's major and specialization",
            "parameters": {
                "type": "object",
                "properties": {
                    "major": {
                        "type": "string",
                        "description": "Major (e.g. 'Computer Science' or 'CS')",
                    },
                    "specialization": {
                        "type": "string",
                        "description": "Specialization (e.g. 'computational perception and robotics' or 'machine learning')",
                    }
                },
                "required": ["major", "specialization"],
            },
        },
        {
            "name": "get_course_assignments",
            "description": "Gets assignments for a course based on the user query",
            "parameters": {
                "type": "object",
                "properties": {
                    "assignment_type": {
                        "type": "string",
                        "description": '''Assignment type depending on due date and submission status. 
                        'Past': 'Old Assignment',
                        'Overdue': 'Past due date',
                        'Undated': 'No due date',
                        'Ungraded': 'Not graded',
                        'Unsubmitted': 'Not submitted',
                        'Upcoming': 'Due in the future',
                        ''',
                        "enum": ['past', 'overdue', 'undated', 'ungraded', 'unsubmitted', 'upcoming']
                    },
                    "course_name": {
                        "type": "string",
                        "description": "Name of the course"
                    }
                },
                "required": ["course_name", "assignment_type"],
            },
        },
        {
            "name": "get_grades",
            "description": "Gets grades for an assignment of a course",
            "parameters": {
                "type": "object",
                "properties": {
                    "course_name": {
                        "type": "string",
                        "description": "Name of the course"
                    },
                    "assignment_name": {
                        "type": "string",
                        "description": "Name of the assignment"
                    }
                },
                "required": ["course_name", "assignment_name"],
            },
        },
        {
            "name": "get_assignment_details",
            "description": "Gets details for an assignment of a course",
            "parameters": {
                "type": "object",
                "properties": {
                    "course_name": {
                        "type": "string",
                        "description": "Name of the course"
                    },
                    "assignment_name": {
                        "type": "string",
                        "description": "Name of the assignment"
                    }
                },
                "required": ["course_name", "assignment_name"],
            },
        }
    ]

    tools = [{"type": "function", "function": fdef} for fdef in function_definitions]

    response = llm.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": query,
            }
        ],
        model="gpt-3.5-turbo",
        tools = tools,
    )

    function_outputs = []

    if response.choices[0].message.tool_calls is None: return ""
    
    for tool_call in response.choices[0].message.tool_calls:
        fname = tool_call.function.name
        fargs = json.loads(tool_call.function.arguments)
        function_response = ""

        if fname == "fetch_professor_data":
            professor_name = fargs['professor_name']
            school_name = 'Georgia Institute of Technology'
            last_name = professor_name.strip().split()[-1]
            function_response = fetch_professor_data(school_name, last_name, professor_name)
        
        elif fname == "get_enrollment_metadata":
            function_response = get_enrollment_metadata(fargs["course_registration_number"])

        elif fname == "get_class_requirements":
            function_response = get_class_requirements(fargs["major"], fargs["specialization"])

        elif tool_call.function.name == "get_grades":
            arguments = json.loads(tool_call.function.arguments)
            function_response = canvas_api.get_grades(arguments['course_name'], arguments['assignment_name'])

        elif tool_call.function.name == "get_course_assignments":
            arguments = json.loads(tool_call.function.arguments)
            if not ('assignment_type' in arguments):
                arguments['assignment_type'] = 'ungraded'
            function_response = canvas_api.get_course_assignments(arguments['course_name'], arguments['assignment_type'])

        elif tool_call.function.name == "get_assignment_details":
            arguments = json.loads(tool_call.function.arguments)
            function_response = canvas_api.get_assignment_details(arguments['course_name'], arguments['assignment_name'])
        
        # Append the function's response
        function_outputs.append(function_response)
    
    if function_outputs is None or not function_outputs: function_outputs = [""]
    function_outputs = f"Relevant information from external API calls: {'. '.join(function_outputs)}"

    return function_outputs

def generate_response(history):
    # Get the latest user message
    user_input = history[-1]["content"]

    if user_input.startswith("Successful File Upload:"):
        # Generate the bot's response based on the file content and special prompt

        # Find the last 'file' entry in history
        file_content = None
        for item in reversed(history):
            if item["role"] == "file":
                file_content = item["content"]
                break
        if file_content is None:
            # No file content found
            bot_response = "An error occurred: No file content found."
            history.append({"role": "bot", "content": bot_response})
            display_history = build_display_history(history)
            return display_history, history

        # Build the special prompt
        prompt = (
            "You are to determine if the following file contents are a syllabus or not. "
            "If the file contents are a syllabus, please output the following message: "
            "'It appears you uploaded the syllabus for the class {class number and name from the syllabus} "
            "here is some key information from this document: "
            "Class Name: {Class Number and Name} \n"
            "Professor: {Professor} \n"
            "Class Contents: {2 sentence summary of the contents of the class} \n"
            "Class Time: {Days of the week and times for the class lectures} \n"
            "Location: {Location of the class} \n"
            "Grade Breakdown: {Grade percentage distribution} \n"
            "Please ask any additional questions you may have about this class!'. "
            "If any of the aforementioned information is not available, please simply put 'Unknown' in the unknown field. "
            "If the file isn't a syllabus you should simply return 'The uploaded file is either not a syllabus or has some other issue, please try again.'\n"
            f"The file contents are:\n{file_content}"
        )

        # Send the prompt to the OpenAI API
        response = query_llm(base_llm, prompt)

        # Add the bot's response to history
        history.append({"role": "bot", "content": response})

        # Build display history
        display_history = build_display_history(history)
        return display_history, history
    else:
        # Proceed as before

        # TODO: ADD MODEL FUNCTION INPUTS
        api_call_data = query_function_calls(base_llm, user_input)

        # Collect all file contents from the history
        file_contents = [item["content"] for item in history if item["role"] == "file"]
        combined_file_content = "\n".join(file_contents) if file_contents else ""
        # Build conversation history excluding 'file' messages and file upload notifications
        conversation_history = ""
        for item in history:
            if item["role"] == "user" and not item["content"].startswith("Successful File Upload:"):
                conversation_history += f"User: {item['content']}\n"
            elif item["role"] == "bot":
                conversation_history += f"Bot: {item['content']}\n"

        rag_data = my_rag.query(user_input, k=3)
        api_data = api_call_data
        query = build_prompt(rag_data, api_data, user_input, conversation_history, combined_file_content)
        response = query_llm(base_llm, query)
        history.append({"role": "bot", "content": response})
        # Build display history
        display_history = build_display_history(history)
        return display_history, history

def add_message(history, message):
    if not isinstance(history, list):
        history = []
    # Handle file uploads
    for file_path in message["files"]:
        file_content = read_file_content(file_path)
        # Store the file content in history with a special role 'file'
        history.append({"role": "file", "content": file_content})
        # Create the file upload success message
        file_name = os.path.basename(file_path)
        truncated_name = truncate_filename(file_name, 20)
        user_message = f"Successful File Upload: {truncated_name}"
        # Add this message to history with role 'user'
        history.append({"role": "user", "content": user_message})
    # Handle text input
    if message["text"] is not None and message["text"].strip() != '':
        history.append({"role": "user", "content": message["text"]})
    return history, gr.update(value=None)  # Clear the textbox

if __name__ == '__main__':
    theme = gr.themes.Soft(
        primary_hue="amber",
        secondary_hue="slate",
    )

    # Initial bot message
    initial_bot_message = (
        "Hello, I am Reggie, the Georgia Tech Registration chatbot. "
        "I am here to help you with any questions you may have about registering for classes at Georgia Tech. "
        "How may I assist you today?"
    )
    # Initialize history as a list of dictionaries
    initial_history = [{"role": "bot", "content": initial_bot_message}]

    # Create the Gradio interface
    with gr.Blocks(theme=theme) as demo:
        # Added header and subtext
        with gr.Row():
            gr.Image(
                value="Georgia_Tech_Buzz_logo.png",
                width=200,
                height=200,
                interactive=False,
                show_label=False,
                show_download_button=False,
            )
            with gr.Column():
                gr.Markdown("# REGGIE - Registration Information Chatbot")
                gr.Markdown(
                    "Reggie is a chatbot aimed to help students register at GT. It can provide useful information, links, and insight into registering for classes at Georgia Tech."
                )
                gr.Markdown(
                    "This project was created by Arjun Verma, Ethan Haarer, Jai Jain, and Ege Gunal."
                )

        # Initialize the chatbot with the initial message, using None for the user message
        chatbot = gr.Chatbot(value=[(None, initial_bot_message)], height=800)
        state = gr.State(initial_history)
        txt = gr.MultimodalTextbox(
            interactive=True,
            file_count="multiple",
            placeholder="Enter message or upload syllabus...",
            show_label=False,
        )

        # When the user submits a message, update the history and clear the textbox
        chat_msg = txt.submit(add_message, [state, txt], [state, txt])

        # Generate response and update the chatbot and state
        bot_msg = chat_msg.then(generate_response, state, [chatbot, state])

    # Launch the Gradio app
    demo.launch()
