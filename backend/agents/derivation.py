from langchain.adapters.openai import convert_openai_messages
from langchain_openai import ChatOpenAI
import json5 as json

sample_json = """
{
  "goal": mathematical formula of current goal,
  "conditions": mathematical formula of conditions that can be used,
  "derivation_process": [
    "mathematical formula 1",
    "mathematical formula 2",
    "mathematical formula 3",
    ],
  "computable_problem": problem computable by wolfram alpha, return None if you can get answer directly
  "derivation_result": answer got after derivation process, return None if you need to use wolfram alpha
}
"""

class DerivationAgent:
    def __init__(self):
        pass

    def derive(self, problem: str, thought: str, progress_summary: str):
        prompt = [{
            "role": "system",
            "content": "You are a math expert. Your sole purpose is to do mathematical derivations based on the given thought"
                       "using rigor mathematical expressions and make derivation using known conditions to make it computable"
                       "by wolfram alpha.\n"
        }, {
            "role": "user",
            "content": f"Problem: {problem}\n"
                       f"Progress_summary: {progress_summary}\n"
                       f"Your Thought: {thought}\n"
                       f"Your task is to do mathematical derivation according to your thought"
                       f"using rigor mathematical expressions and make derivations using known conditions to make it computable.\n"
                       f"First of all, check if the thought can be directly finished by wolfram alpha, if so 'derivation_process' field should contain thought as computable_problem.\n"
                       f"Then, check if you can get the answer by derivation, if do not use wolfram alpha and the 'computable_problem' should be None"
                       f"Do not compute complicate expressions in yourself, only simplify them to make it computable by"
                       f"wolfram alpha\n"
                       f"Please return nothing but a JSON in the following format, 'derivation_process' field should be None if not necessary:\n"
                       f"{sample_json}\n "

        }]

        lc_messages = convert_openai_messages(prompt)
        optional_params = {
            "response_format": {"type": "json_object"}
        }

        response = ChatOpenAI(model='gpt-4-0125-preview', max_retries=1, model_kwargs=optional_params).invoke(lc_messages).content
        return json.loads(response)
    
    def run(self, progress_info: dict):
        problem = progress_info.get("problem")
        progress = progress_info.get("progress")
        
        derivation_info = self.derive(problem, progress["rethoughts"][-1], progress["progress_summary"][-1])
        if "derivation_info" not in progress_info:
            progress_info["derivation_info"] = [derivation_info]
        else:
            progress_info["derivation_info"].append(derivation_info)
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
    derivation_agent = DerivationAgent()
    updated_progress_info = derivation_agent.run(progress_info)
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
            "computation_result": 'Assumption: factor | 135135 \nAnswer: 3^3×5×7×11×13 (7 prime factors, 5 distinct)'
        }]
    }
    updated_progress_info = derivation_agent.run(progress_info)
    print(updated_progress_info)