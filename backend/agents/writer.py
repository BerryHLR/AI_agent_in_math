from langchain.adapters.openai import convert_openai_messages
from langchain_openai import ChatOpenAI
import json5 as json

sample_json = """
{
  "title": title of the article,
  "paragraphs": [
    "paragraph 1",
    "paragraph 2",
    "paragraph 3",
    "paragraph 4",
    "paragraph 5",
    ],
    "summary": "2 sentences summary of the article"
}
"""

class WriterAgent:
    def __init__(self):
        pass

    def write(self, material: dict):
        prompt = [{
            "role": "system",
            "content": "You are a excellent explanatory blog writer. "
                       "Your sole purpose is to write a well-written and engaging article about how to solve a math problem"
                       "based on the material provided to you. The article should contain the final answer of the problem.\n"
                       "Your should using Latex for math formula"
        }, {
            "role": "user",
            "content": f"Material: {material}\n"
                       f"Your task is to write a well-written article about how to solve a math problem"
                       f"based on the material provided to you. The article should contain the final answer of the problem.\n"
                       f"Please return nothing but a JSON in the following format.\n"#, the content should be chinese in UTF-8:\n"
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
        material = progress_info.get("explanation")
        article = self.write(material)
        return article

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
          'computation_result': 'Answer: 55'}],
        'explanation': {
            'problem': 'Find the sum of five consecutive odd numbers whose product is 135135.',
            'key_steps': [
                {
                    'step': 'Perform prime factorization of 135135.',
                    'motivation': 'Prime factorization helps in identifying the pattern of numbers and their possible arrangements, especially for consecutive numbers.',
                    'background_knowledge': 'Prime factorization is the breakdown of a composite number into a product of prime numbers.',
                    'process_and_result': 'Prime factorization of 135135 results in 3^3×5×7×11×13.'
                },
                {
                    'step': 'Identify the pattern of five consecutive odd numbers from the prime factors.',
                    'motivation': 'By examining the prime factors, we can determine the range of the consecutive odd numbers, considering that their product has to match the prime factorization.',
                    'background_knowledge': 'Consecutive odd numbers have a common difference of 2. The product of such numbers is influenced by their individual factors.',
                    'process_and_result': "Given the prime factorization, 3^3×5×7×11×13, and knowing we are dealing with consecutive odd numbers, it's logical to center our sequence around the middle prime factor. Selecting 11 as the central number leads to the sequence: 7, 9, 11, 13, 15."
                },
                {
                    'step': 'Compute the sum of the identified sequence.',
                    'motivation': 'After identifying the sequence, summing these numbers provides the solution to the problem.',
                    'background_knowledge': 'The sum of a sequence of numbers can be directly calculated by adding them together.',
                    'process_and_result': 'Sum of the sequence 7, 9, 11, 13, 15 is calculated as 55.'
                }
            ]
        }  
    }
    writer_agent = WriterAgent()
    article = writer_agent.run(progress_info)
    print(article)