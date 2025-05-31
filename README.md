## REGGIE: The Georgia Tech Registration Chatbot
This repo contains the code, files and evaulation metrics used to create and assess the efectiveness of the REGGIE chatbot developed by Arjun Verma, Ethan Haarer, Ege Gunal and Jai Jain for the final project of CS 8803 - Conversational AI. This chatbot has been preloaded with information about Georgia Tech's class registration system, and can access real time data from other sites to inform students about class choices.

Some Choice Features Include:
- Given CRNs, can return how many open seats are in a given class
- May return a professor's RateMyProfessor statistics when asked about the quality of Professors
- Can processes syllabi to retrieve core class information and answer student queries about uploaded documents
- May supply class requirements for seclect majors and specializations
- Point users towards useful links and pages for further information

An active version of Reggie can be found here: https://huggingface.co/spaces/RangDeBasanti/Reggie

## Usage

First, clone the repository and use git lfs to pull down the RAG_data pdfs. In order to build the RAG itself, run RAG.py. As well as this, you have to create a file called "OPENAI_KEY.txt" with a valid OpenAI API key in it as well as a file called "CANVAS_KEY.txt" with a valid Canvas API key in it. From there, you can run "python ChatbotUI.py" in order to run the system locally.

## Results

Our base evaluation results can be found in the "eval_results" folder or can be recalculated locally by running the "LLMEval.py" file. 
