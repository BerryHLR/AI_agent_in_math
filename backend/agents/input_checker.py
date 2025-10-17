from langchain.adapters.openai import convert_openai_messages
from langchain_openai import ChatOpenAI

class InputCheckerAgent:
    def __init__(self):
        pass

    def check(self, problem: str):
        prompt = [{
            "role": "system",
            "content": "Your sole purpose is to check whether the input is a valid math problem."
                       "If not, tell the user to correct their input\n "
        }, {
            "role": "user",
            "content": f"Problem: {problem}\n"
                       f"Your task is to check whether the input is a valid math problem."
                       f"If not, tell the user to correct their input. However, return None if the problem is valid\n"
                       f"Please response in the language of input"
        }]

        lc_messages = convert_openai_messages(prompt)

        response = ChatOpenAI(openai_api_key='your_key',model='gpt-4-0125-preview', max_retries=3).invoke(lc_messages).content
        print(response)
        return response
    
    def run(self, progress_info: dict):
        problem = progress_info.get("problem")
        response = self.check(problem)
        progress_info["check_result"] = response
        return progress_info

if __name__ == "__main__":
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv())
    progress_info = {
        "problem": "商店里有239包薯片，卖出一些后，还剩21包，后来又运进187包，现在商店有薯片多少包？"
    }
    input_checker_agent = InputCheckerAgent()
    updated_progress_info = input_checker_agent.run(progress_info)
