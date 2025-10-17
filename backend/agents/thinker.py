from langchain.adapters.openai import convert_openai_messages
from langchain_openai import ChatOpenAI
import json5 as json

sample_json = """
{
  "thought": what to do next in one sentence
  "progress_summary": current progress in short summary, None if no progress
  "is_final": return 'True' if already got final answer, else 'False'
}
"""
class ThinkerAgent:
    def __init__(self):
        pass
    def think(self, problem: str, previous_thought: str | None, previous_result: str | None, feedback: dict | None):

        prompt = [{
            "role": "system",
            "content": "You are a math expert. Your sole purpose is to think about what to do next"
                       "for solving the question you are given based on current progress and feedback.\n "
        }, {
            "role": "user",
            "content": f"Question: {problem}\n"
                       f"Previous thought: {previous_thought}\n"
                       f"Previous result: {previous_result}\n"
                       f"feedback : {feedback}\n"
                       f"Your task is to think about what to do next for solving the question"
                       f"you are given based on current progress and feedback.\n "
                       f"Please return nothing but a JSON in the following format:\n"
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
        if progress is not None:
            # 获取之前最近的thought和rethought, 如果有rethought则使用rethought, 否则使用thought
            previous_thought = progress.get("thoughts")[-1]
            previous_rethoughts = progress.get("rethoughts")

            if previous_rethoughts is not None:
                previous_rethought = previous_rethoughts[-1]
                previous_result = progress_info.get("derivation_info")[-1].get("result")
                feedback = progress_info.get("derivation_info")[-1].get("feedback")
                thought = self.think(problem, previous_rethought, previous_result, feedback)
            else:
                # 假设没有rethought则没经过计算过程，没有result
                thought = self.think(problem, previous_thought, None, None)

            progress["thoughts"].append(thought["thought"])
            progress["progress_summary"].append(thought["progress_summary"])
            progress_info["progress"] = progress
            progress_info["is_final"] = thought["is_final"]
        else:
            thought = self.think(problem, None, None, None)
            progress = {
                "thoughts": [thought["thought"]],
                "progress_summary": [thought["progress_summary"]]
            }
            progress_info["progress"] = progress
        return progress_info

if __name__ == "__main__":
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv())
    progress_info = {
        "problem": "如果5个连续奇数的乘积为135135，那么这5个数的和是多少",
    }
    thinker_agent = ThinkerAgent()
    updated_progress_info = thinker_agent.run(progress_info)
    print(updated_progress_info)
    # 测试连续两次think的结果
    final_progress_info = thinker_agent.run(updated_progress_info)
    print(final_progress_info)

    # 测试thinker对第二轮输入的响应
    progress_info = {
        "problem": "如果5个连续奇数的乘积为135135，那么这5个数的和是多少",
        "progress": {
            "thoughts": ["find the five consecutive odd numbers whose product is 135135, and then sum them up"],
            "progress_summary": ["None"],
            "rethoughts": ["Consider prime factorization of 135135 to identify the pattern of five consecutive odd numbers and calculate their sum more efficiently."]
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
    updated_progress_info = thinker_agent.run(progress_info)
    print(updated_progress_info)

    # 检查是否能判断结束
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
          'result': 'Answer: 55'}]
    }
    updated_progress_info = thinker_agent.run(progress_info)
    print(updated_progress_info)
    