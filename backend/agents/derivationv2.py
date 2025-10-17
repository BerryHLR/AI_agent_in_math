from langchain_experimental.tools import PythonREPLTool
from langchain.agents import AgentExecutor
from langchain import hub
from langchain.agents import create_react_agent
from langchain_openai import ChatOpenAI
from langchain.chains import LLMCheckerChain
from langchain.tools import tool

instructions = """You are an agent designed to use mathematical expressions to solve math problems step by step.
You have access to a math checker, which you can use to check the rightness of each step.
If you get an wrong feedback, correct your last step and try again.
If it seems like the problem is missing conditions so you can not solve , just return "I don't know" as the answer.
"""

base_prompt = hub.pull("langchain-ai/react-agent-template")
prompt = base_prompt.partial(instructions=instructions)
llm = ChatOpenAI(model='gpt-4-0125-preview', max_retries=3)
checker_chain = LLMCheckerChain.from_llm(llm, verbose=True)

input = """
"problem": "如果5个连续奇数的乘积为135135，那么这5个数的和是多少",
        "progress": {
            "thoughts": ["find the five consecutive odd numbers whose product is 135135, and then sum them up", "Identify the middle number of the five consecutive odd numbers by looking at the prime factors and their possible arrangements."],
            "progress_summary": ["None", "Prime factorization of 135135 has been identified as 3^3×5×7×11×13, which are the prime factors that need to be arranged into five consecutive odd numbers."],
            "rethoughts": ["Consider prime factorization of 135135 to identify the pattern of five consecutive odd numbers and calculate their sum more efficiently.", "Consider the pattern of multiplication of five consecutive odd numbers and the distribution of their prime factors, particularly focusing on the highest and lowest factors to determine the range."]
        }
"""
@tool
def math_checker(step: str) -> str:
    """check derivation step based on llm"""
    result = checker_chain.invoke(step)
    return result

class ComputationAgent:
    def __init__(self):
        self.llm = ChatOpenAI(model='gpt-4-0125-preview', max_retries=3)
        self.tools = [math_checker]
        self.agent = create_react_agent(self.llm, self.tools, prompt)
        self.agent_executor = AgentExecutor(agent=self.agent, tools=self.tools, verbose=True)
        
    def compute(self, computable_problem: str):
        computation_result = self.agent_executor.invoke({"input": input})
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