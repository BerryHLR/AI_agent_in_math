from langchain.adapters.openai import convert_openai_messages
from langchain_openai import ChatOpenAI
import json5 as json

sample_json = """
{
  "question": your question
  "reason": your reason
}
"""
class QuestionerAgent:
    def __init__(self):
        pass
    def question(self, problem: str, thought: str, analysis: str):

        prompt = [{
            "role": "system",
            "content": "You are a math expert with a sharp mind and keen observation skills, adept at identifying errors.\n"
                       "Your sole purpose is to question the thoughts and analysis process on a certain problem"
                       "and to pose a valuable question.\n "
        }, {
            "role": "user",
            "content": f"Problem: {problem}\n"
                       f"Other's thought: {thought}\n"
                       f"Other's analysis: {analysis}\n"
                       f"Your task is to question the thoughts and analysis process on a certain problem"
                       f"and to pose a valuable question.\n"
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
        thought = progress.get("rethoughts")[-1]
        analysis = progress_info.get("derivation_info")[-1].get("analysis")
        feedback = self.question(problem, thought, analysis)
        if "feedback" not in progress_info:
            progress_info["feedback"] = [feedback]
        else:
            progress_info["feedback"].append(feedback)
        return progress_info

if __name__ == "__main__":
    from dotenv import load_dotenv, find_dotenv
    load_dotenv(find_dotenv())
    progress_info = {
        "problem": "一个圆柱体的玻璃缸里面有一些水，把一个底面积25平方厘米的长方体全部放入水中，玻璃缸中的水位上升4厘米，如果长方体沿着高露出水面6厘米，缸中的水面下降2厘米，则长方体的体积是多少立方厘米",
        "progress": {
            "thoughts": ["Calculate the volume of water displaced by the long rectangular solid using the area of its base and the change in water level when submerged."],
            "progress_summary": "None",
            "rethoughts": ["Determine the volume of the rectangular solid by calculating the volume of water displaced when it is fully submerged, then adjust this calculation to account for the additional information about the water level change when part of the rectangular solid is above water."]
        },
        "derivation_info": [{
            "analysis": "To find the volume of the rectangular solid, we first consider the scenario where the solid is fully submerged in the water. The water level rises 4 cm when the solid is submerged, and the base area of the solid is 25 square centimeters, indicating that the volume of water displaced by the solid equals its volume. The formula for the volume of a displaced liquid (and thus the solid) is the area of the base multiplied by the height of the water level rise, which in this case is the rise when the solid is fully submerged. Thus, the initial volume calculation would be 25 cm^2 * 4 cm. Next, we take into account the information that when the solid is partially submerged with 6 cm above water, the water level drops by 2 cm. This change suggests a relationship between the volume of the part of the solid submerged and the volume of the cylinder up to the new water level. However, this information is used to confirm the displacement effect of the solid on the water level, not directly in calculating its volume. The initial calculation based on the full submersion provides the direct method to find the volume of the solid.",
            "computable_problem": "25 cm^2 * 4 cm"
        }]
    }
    questioner_agent = QuestionerAgent()
    updated_progress_info = questioner_agent.run(progress_info)

    