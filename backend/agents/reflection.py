from langchain.adapters.openai import convert_openai_messages
from langchain_openai import ChatOpenAI
import json5 as json

sample_json = """
{
  "rethought": what to do next in one sentence
}
"""

class ReflectionAgent:
    def __init__(self):
        pass

    def reflect(self, thought: str, problem: str, progress_summary: str):
        prompt = [{
            "role": "system",
            "content": "You are a math expert. Your sole purpose is to criticize the usefulness of thought"
                       "for solving the problem and try to give a better thought. However, if the thought is useful enought, do not change it. \n "
        }, {
            "role": "user",
            "content": f"Problem: {problem}\n"
                       f"Progress: {progress_summary}\n"
                       f"Thought: {thought}\n"
                       f"Your task is to criticize the usefulness of thought"
                       f"based on problem and current progress and try to give a better thought.\n "
                       f"Please return nothing but a JSON in the following format:\n"
                       f"{sample_json}\n"
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

        rethought = self.reflect(progress["thoughts"][-1], problem, progress["progress_summary"])
        
        if progress.get("rethoughts") is not None:
            progress["rethoughts"].append(rethought["rethought"])
        else:
            progress = {
                "rethoughts": [rethought["rethought"]]
            }
            progress_info["progress"].update(progress)
        return progress_info

if __name__ == "__main__":
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv())
    progress_info = {
        "problem": "如果5个连续奇数的乘积为135135，那么这5个数的和是多少",
        "progress": {
            "thoughts": ["Find the prime factorization of 135135 to understand the structure of the product."],
            "progress_summary": "None"
        }
    }
    reflection_agent = ReflectionAgent()
    updated_progress_info = reflection_agent.run(progress_info)
    print(updated_progress_info)

    # 测试reflection_agent对第二轮输入的响应
    progress_info = {
        "problem": "如果5个连续奇数的乘积为135135，那么这5个数的和是多少",
        "progress": {
            "thoughts": ["find the five consecutive odd numbers whose product is 135135, and then sum them up", "Identify the middle number of the five consecutive odd numbers by looking at the prime factors and their possible arrangements."],
            "progress_summary": ["None", "Prime factorization of 135135 has been identified as 3^3×5×7×11×13, which are the prime factors that need to be arranged into five consecutive odd numbers."],
            "rethoughts": ["Consider prime factorization of 135135 to identify the pattern of five consecutive odd numbers and calculate their sum more efficiently."]
        },
        "derivation_info": {
            "goal": "Sum = n + (n+2) + (n+4) + (n+6) + (n+8)",
            "conditions": "Product = n * (n+2) * (n+4) * (n+6) * (n+8) = 135135",
            "derivation_process": [
                "Prime factorization of 135135",
                "Identify pattern of five consecutive odd numbers from prime factors",
                "Compute sum of these five numbers"
            ],
            "computable_problem": "prime factorization of 135135",
            "result": 'Assumption: factor | 135135 \nAnswer: 3^3×5×7×11×13 (7 prime factors, 5 distinct)'
        }
    }
    updated_progress_info = reflection_agent.run(progress_info)
    print(updated_progress_info)