from RAG import GT_RAG
from openai import OpenAI
from ChatbotUI import generate_response, query_llm
import json

class Evaluator():
    def __init__(self):
        openai_key = open('OPENAI_KEY.txt').read().strip()
        self.eval_llm = OpenAI(api_key=openai_key)

    def evaluate_question_response(self, query : str, gt_chat_response: str):
        evaluator_system_prompt = f'Your name is Dr. GT, and your sole purpose is to evaluate the quality of responses provided by\
        the Georgia Tech Registration Chatbot. You will grade the quality of responses of this chatbot on a scale of 1 to 10\
        based off the completeness and accuracy of its response to the question it was asked. The chatbot should respond with\
        specific data, not vague references and answers.'

        evaluator_prompt = f'Question asked: [{query}]. Response from Georgia Tech Registration Chatbot: [{gt_chat_response}]. Grade\
        the response from the Georgia Tech Registration Chatbot to the question asked on a scale of 1 to 10. Return this grade as\
        the "grade" member of a JSON object and your explanation for this grade as the "explanation" member.'

        evaluation = self.eval_llm.chat.completions.create(
            messages=[
                {"role": "system", "content": evaluator_system_prompt},
                {"role": "user", "content": evaluator_prompt}
            ],
            model="gpt-3.5-turbo",
            response_format={"type": "json_object"}
        )

        evaluation = json.loads(evaluation.choices[0].to_dict()['message']['content'])
        evaluation['response'] = gt_chat_response

        return evaluation

def build_history(query):
    return [{
        "content": query,
        "role": "user"
    }]

if __name__ == '__main__':
    eval = Evaluator()

    eval_questions = [
        "Tell me about my new professor for CS 3600, Thad Starner",
        "Are there available seats for the CS 3600, CRN 30312",
        "Where can I find information regarding registration?",
        "What courses should I take as a Machine Learning masters student in computer science?",
        "Tell me about my new professor for SysML, Alexey tumanov",
        "I'm worried I won't be able to register for classes on time - what's the deadline for registering?",
        "Can the office tell me which courses I can currently take?",
        "What does it mean if I get an error when I try to register for a course?",
        "If I can't register until after registration ends what happens to me?",
        "Am I gonna be waitlisted for my CRN 32394 course?",
        "Oh shoot I missed my waitlist notification - what now?",
        "What's the difference between Phase one and Phase two registration?",
        "I need my tuition waiver and I've completed GradWorks - what now?",
        "When do I get paid as a TA?",
        "What class should I register for as a GRA/GTA?",
        "How can I change my master's specialization?",
        "Tell me about what I should take as a masters student in computer science with a concentration in computing systems",
        "How can I register as a ms cs student?",
        "What should I do if I can't register for a class anymore?",
        "Should I be a mscs student? Idk if I can handle too many courses"
    ]

    gt_chatbot_evaluations = []
    base_llm_evaluations = []

    for q in eval_questions:
        gt_chat_response = generate_response(build_history(q))
        gt_chatbot_evaluations.append(eval.evaluate_question_response(q, gt_chat_response))

        base_chat_response = query_llm(eval.eval_llm, q)
        base_llm_evaluations.append(eval.evaluate_question_response(q, base_chat_response))
    
    print(f'GT Chatbot Average Score: {sum([r["grade"] for r in gt_chatbot_evaluations]) / len(gt_chatbot_evaluations)}')
    print(f'Base LLM Average Score: {sum([r["grade"] for r in base_llm_evaluations]) / len(base_llm_evaluations)}')

    with open("gt_chatbot_evaluations.json", "w") as f:
        gt_chatbot_evaluations = {f'Response: {i}' : e for i, e in enumerate(gt_chatbot_evaluations)}
        json.dump(gt_chatbot_evaluations, f)

    with open("base_llm_evaluations.json", "w") as f:
        base_llm_evaluations = {f'Response: {i}' : e for i, e in enumerate(base_llm_evaluations)}
        json.dump(base_llm_evaluations, f)
