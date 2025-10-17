from langchain.adapters.openai import convert_openai_messages
from langchain_openai import ChatOpenAI
import json5 as json

sample_json = """
{
  "needs_mathematical_derivation_or_computation",
  "can_be_solved_by_simple_analysis"
}
"""
wolfram_alpha_intro = """
What Wolfram Alpha Can Do:
1. Algebra: Solve equations and inequalities, factor polynomials, simplify expressions, and perform algebraic manipulations.
2. Calculus: Differentiate and integrate functions, including definite and indefinite integrals. It can also solve differential equations and perform series expansions.
3. Geometry: Compute properties of geometric figures, such as area, perimeter, and volume. It can also work with geometric transformations.
4. Statistics and Data Analysis: Perform statistical computations, including descriptive statistics, probability distributions, and hypothesis testing.
5. Linear Algebra: Solve systems of linear equations, compute determinants, inverses, eigenvalues, and eigenvectors of matrices.
6. Number Theory: Work with prime numbers, modular arithmetic, and perform number theoretic functions.
7. Discrete Mathematics: Solve problems related to graph theory, permutations, combinations, and logic puzzles.
8. Mathematical Functions: Evaluate and plot a wide range of mathematical functions
What Wolfram Alpha Cannot Do:
1. Solving Problems with Insufficient Information: If the problem lacks enough information or is too ambiguous, Wolfram Alpha might not be able to provide a solution.
2. Interpreting Poorly Formulated Questions: While it's good at understanding natural language, poorly formulated or highly ambiguous questions can lead to incorrect or irrelevant answers.
3. Advanced Theoretical Mathematics: While Wolfram Alpha is powerful, it might struggle with highly advanced or niche areas of mathematics that require deep theoretical insights or are at the forefront of mathematical research.
"""

class JudgerAgent:
    def __init__(self):
        pass

    def judge(self, problem: str, thought: str, progress_summary: str):
        prompt = [{
            "role": "system",
            "content": "Your sole purpose is to judge whether a problem needs rigor mathematical transformation"
                       "or can be directly solved by yourself.\n"
        }, {
            "role": "user",
            "content": f"Problem: {problem}\n"
                       f"Progress_summary: {progress_summary}\n"
                       f"Your Thought: {thought}\n"
                       f"Your task is to judge whether a problem needs rigor mathematical transformation"
                       f"or can be directly solved by yourself.\n"
                       f"Please return nothing but a string from one of the two options:\n"
                       f"{sample_json}\n "

        }]

        lc_messages = convert_openai_messages(prompt)
        

        response = ChatOpenAI(model='gpt-4-0125-preview', max_retries=1).invoke(lc_messages).content
        return json.loads(response)
    
    def run(self, progress_info: dict):
        problem = progress_info.get("problem")
        progress = progress_info.get("progress")
        
        judge_result = self.judge(problem, progress["rethoughts"][-1], progress["progress_summary"][-1])
        if "judge_result" not in progress_info:
            progress_info["judge_result"] = [judge_result]
        else:
            progress_info["judge_result"].append(judge_result)
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
    judge_agent = JudgerAgent()
    updated_progress_info = judge_agent.run(progress_info)
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
    updated_progress_info = judge_agent.run(progress_info)
    print(updated_progress_info)