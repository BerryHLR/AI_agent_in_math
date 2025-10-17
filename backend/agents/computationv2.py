from langchain_experimental.llm_symbolic_math.base import LLMSymbolicMathChain
from langchain_openai import ChatOpenAI

class ComputationAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model='gpt-4-0125-preview', max_retries=3)
        self.llm_symbolic_math = LLMSymbolicMathChain.from_llm(self.llm)
    def compute(self, computable_problem: str):
        computation_result = self.llm_symbolic_math.invoke({"question": computable_problem})
        print(computation_result)
        return computation_result

    def run(self, progress_info: dict):
        if progress_info["derivation_info"][-1].get("computable_problem") is None:
            return progress_info
        computable_problem = progress_info["derivation_info"][-1]["computable_problem"]
        computation_result = self.compute(computable_problem)
        progress_info["derivation_info"][-1]["result"] = computation_result
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
        },
        "derivation_info": [{
            "goal": "Sum = n + (n+2) + (n+4) + (n+6) + (n+8)",
            "conditions": "Product = n * (n+2) * (n+4) * (n+6) * (n+8) = 135135",
            "derivation_process": [
                "Prime factorization of 135135",
                "Identify pattern of five consecutive odd numbers from prime factors",
                "Compute sum of these five numbers"
            ],
            "computable_problem": "Solve the system of equations: E_A = 1/2 * (E_B + 1), E_B = 1/2 * E_A"
        }]
    }

    computation_agent = ComputationAgent()
    updated_progress_info = computation_agent.run(progress_info)
    print(updated_progress_info)

    # 测试computation_agent对第二轮输入的响应
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
        {'goal': 'Sum of 5 consecutive odd numbers', 
         'conditions': 'Product = 3^3 * 5 * 7 * 11 * 13', 
         'derivation_process': [
            'Let the middle number in the sequence of five consecutive odd numbers be x', 
            'Thus, the five numbers are (x-4), (x-2), x, (x+2), (x+4)', 
            'Product = (x-4)*(x-2)*x*(x+2)*(x+4)', 
            'Given Product = 3^3 * 5 * 7 * 11 * 13', 
            'To find: Sum = (x-4) + (x-2) + x + (x+2) + (x+4) = 5x'
            ], 
            'computable_problem': 'Solve (x-4)*(x-2)*x*(x+2)*(x+4) = 3^3 * 5 * 7 * 11 * 13 for x', 
            'computation_result': None}]
    }
    updated_progress_info = computation_agent.run(progress_info)
    print(updated_progress_info)