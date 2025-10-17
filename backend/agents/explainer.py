from langchain.adapters.openai import convert_openai_messages
from langchain_openai import ChatOpenAI
import json5 as json

sample_json = """
{
  "problem": restate of the problem in short summary
  "key_steps": [
    {
      "step": what to do in one sentence,
      "motivation": goal of this step and benefits specific to this problem,
      "background_knowledge": math theorem or techniques need to know, None if nothing important,
      "process_and_result": exact math derivation process and result, only output math expressions 
    }
  ]
}
"""

class ExplainerAgent:
    def __init__(self):
        pass

    def explain(self, problem: str, rethoughts: [str], derivation_info: dict):
        prompt = [{
            "role": "system",
            "content": "You are a math teacher expert in explaining in simple yet accurate terms. "
                       "Your sole purpose is to explain how to solve a math problem"
                       "and why doing each step based on the solving process you are given.\n"
        }, {
            "role": "user",
            "content": f"Problem: {problem}\n"
                       f"Thinking process of solving the problem: {rethoughts}"
                       f"Math derivation of each thought: {derivation_info}\n"
                       f"Your task is to explain how to solve this math problem"
                       f"and why doing each step based on the solving process you are given.\n"
                       f"Please return nothing but a JSON in the following format, each key step should correspond to one thought\n"
                       f"{sample_json}\n "

        }]

        lc_messages = convert_openai_messages(prompt)
        optional_params = {
            "response_format": {"type": "json_object"}
        }

        response = ChatOpenAI(model='gpt-4-0125-preview', max_retries=3, model_kwargs=optional_params).invoke(lc_messages).content
        print(json.loads(response))
        return json.loads(response)
    
    def run(self, progress_info: dict):
        problem = progress_info.get("problem")
        progress = progress_info.get("progress")
        
        explanation = self.explain(problem, progress["rethoughts"], progress_info["derivation_info"])
        progress_info["explanation"] = explanation
        return progress_info

if __name__ == "__main__":
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv())
    progress_info = {
        "problem": "如果5个连续奇数的乘积为135135，那么这5个数的和是多少",
        "progress": {
            "thoughts": ["find the five consecutive odd numbers whose product is 135135, and then sum them up", "Identify the middle number of the five consecutive odd numbers by looking at the prime factors and their possible arrangements."],
            "progress_summary": ["None", "Prime factorization of 135135 has been identified as 3^3×5×7×11×13, which are the prime factors that need to be arranged into five consecutive odd numbers."],
            "rethoughts": ["Consider prime factorization of 135135 to identify the pattern of five consecutive odd numbers and calculate their sum more efficiently.", "Consider the pattern of multiplication of five consecutive odd numbers and the distribution of their prime factors, particularly focusing on the highest and lowest factors to determine the range."]
        },
        "derivation_info": [{
            "goal": "Sum = n + (n+2) + (n+4) + (n+6) + (n+8)",
            "conditions": "Product = n * (n+2) * (n+4) * (n+6) * (n+8) = 135135",
            "derivation_process": [
                "Prime factorization of 135135",
                "Identify pattern of five consecutive odd numbers from prime factors",
                "Compute sum of these five numbers"
            ],
            "computable_problem": "prime factorization of 135135",
            "computation_result": 'Assumption: factor | 135135 \nAnswer: 3^3×5×7×11×13 (7 prime factors, 5 distinct)'
        },
        {'goal': 'Sum = n + (n+2) + (n+4) + (n+6) + (n+8)', 
         'conditions': 'n*(n+2)*(n+4)*(n+6)*(n+8) = 135135', 
         'derivation_process': [
            'Prime factorization of 135135 = 3^3*5*7*11*13', 
            'Identify sequence of 5 consecutive odd numbers: Since the product includes prime factors up to 13, consider the middle number to be 11 (5th prime number), making the sequence 7, 9, 11, 13, 15', 
            'Compute sum of the identified sequence: 7 + 9 + 11 + 13 + 15'
            ], 
          'computable_problem': '7 + 9 + 11 + 13 + 15', 
          'derivation_result': None,
          'computation_result': 'Answer: 55'}]
    }
    explainer_agent = ExplainerAgent()
    updated_progress_info = explainer_agent.run(progress_info)
    print(updated_progress_info)
