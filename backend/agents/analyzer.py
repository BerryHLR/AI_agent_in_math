from langchain.adapters.openai import convert_openai_messages
from langchain_openai import ChatOpenAI
import json5 as json

sample_json = """
{
  "analysis": the process of your thinking
  "result": final answer.
}
"""

sample_json2 = """
{
  "analysis": the process of your thinking
  "computable_problem": computable problem after your thinking
}
"""


class AnalyzerAgent:
    def __init__(self):
        pass

    def analyze(self, problem: str, thought: str, progress_summary: str):
        prompt = [{
            "role": "system",
            "content": "Your are a math expert. Your sole purpose is to try to analyze the problem step by step"
                       "based on current progress and your own thought.\n"
        }, {
            "role": "user",
            "content": f"Problem: {problem}\n"
                       f"Progress_summary: {progress_summary}\n"
                       f"Your Thought: {thought}\n"
                       f"Your task is to analyze the problem step by step"
                       f"based on current progress and your own thought.\n"
                       f"If you can get the final answer without computation, return nothing but a JSON in the following format:\n"
                       f"{sample_json}\n "
                       f"However if you need to do computation, return in the following format:\n"
                       f"{sample_json2}\n"

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
        
        analysis = self.analyze(problem, progress["rethoughts"][-1], progress["progress_summary"][-1])
        if "derivation_info" not in progress_info:
            progress_info["derivation_info"] = [analysis]
        else:
            progress_info["derivation_info"].append(analysis)
        return progress_info

if __name__ == "__main__":
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv())
    progress_info = {
        "problem": "如果5个连续奇数的乘积为135135，那么这5个数的和是多少",
        "progress": {
            "thoughts": ["find the five consecutive odd numbers whose product is 135135, and then sum them up"],
            "progress_summary": "None",
            "rethoughts": ["Consider prime factorization of 135135 to identify the pattern of five consecutive odd numbers and calculate their sum more efficiently."]
        }
    }
    analyze_agent = AnalyzerAgent()
    updated_progress_info = analyze_agent.run(progress_info)
    print(updated_progress_info)

    # 测试derivation_agent对第二轮输入的响应
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
            "result": 'Assumption: factor | 135135 \nAnswer: 3^3×5×7×11×13 (7 prime factors, 5 distinct)'
        }]
    }
    updated_progress_info = analyze_agent.run(progress_info)
    print(updated_progress_info)