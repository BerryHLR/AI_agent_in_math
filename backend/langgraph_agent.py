import os
import time
from concurrent.futures import ThreadPoolExecutor
from langgraph.graph import Graph, END
import sys



# sys.path.append(r'D:\Berry\UROP\2023 spring\NewFramework\backend')
# sys.path.append(r'D:\Berry\UROP\2023 spring\NewFramework\backend\agents')

# Import agent classes
from agents import (
    DesignerAgent,
    ThinkerAgent,
    AnalyzerAgent,
    InputCheckerAgent,
    JudgerAgent,
    QuestionerAgent,
    ReflectionAgent,
    DerivationAgent,
    ComputationAgent,
    ExplainerAgent,
    WriterAgent,
    EditorAgent,
    PublisherAgent,
)


class MasterAgent:
    def __init__(self):
        self.output_dir = f"outputs/run_{int(time.time())}"
        os.makedirs(self.output_dir, exist_ok=True)
        pass

    def run(self, queries: list, layout: str = "layout_3.html"):
        # Initialize agents
        input_checker_agent = InputCheckerAgent()
        thinker_agent = ThinkerAgent()
        reflection_agent = ReflectionAgent()
        writer_agent = WriterAgent()
        derivation_agent = DerivationAgent()
        computation_agent = ComputationAgent()
        explainer_agent = ExplainerAgent()
        judger_agent = JudgerAgent()
        analyzer_agent = AnalyzerAgent()
        questioner_agent = QuestionerAgent()

        # designer
        designer_agent = DesignerAgent(self.output_dir)
        # frontend
        editor_agent = EditorAgent(layout)
        publisher_agent = PublisherAgent(self.output_dir)

        # Define a Langchain graph
        workflow = Graph()

        # Add nodes for each agent
        workflow.add_node("input_check", input_checker_agent.run)
        workflow.add_node("think", thinker_agent.run)
        workflow.add_node("reflect", reflection_agent.run)
        # workflow.add_node("derive", derivation_agent.run)
        workflow.add_node("compute", computation_agent.run)
        workflow.add_node("explain", explainer_agent.run)
        workflow.add_node("write", writer_agent.run)
        # workflow.add_node("judge", judger_agent.run)
        workflow.add_node("analyze", analyzer_agent.run)
        workflow.add_node("question", questioner_agent.run)
        workflow.add_node("design", designer_agent.run)

        def should_continue(state):
            # print(state)
            x = state.get("is_final")
            # print(x)
            if x == "True":
                return "finish"
            else:
                return "continue"

        def should_continue2(state):
            print(state)
            x = state.get("judge_result")[-1]
            print(x)
            if x == "needs_mathematical_derivation_or_computation":
                return "derive"
            else:
                return "analyze"

        def should_continue3(state):
            print(state)
            x = state.get("derivation_info")[-1]["computable_problem"]
            print(x)
            if x is not None:
                return "compute"
            else:
                return "think"

        def should_continue4(state):
            # print(state)
            x = state.get("check_result")
            # print(x)
            if x == "None":
                return "continue"
            else: return "stop"

        # 将should_continue替换成下列函数即可不显示输出：lambda x: "finish" if x.get("is_final") == "True" else "continue"
        # Set up edges
        workflow.add_conditional_edges(start_key='input_check',
                                       condition=should_continue4,
                                       conditional_edge_mapping={"stop": END, "continue": "think"})
        workflow.add_edge("reflect", "analyze")
        workflow.add_edge("analyze", "compute")
        workflow.add_edge("compute", "question")
        workflow.add_edge("question", "think")
        workflow.add_conditional_edges(
            start_key="think",
            condition=should_continue,
            conditional_edge_mapping={"finish": "explain", "continue": "reflect"},
        )
        workflow.add_edge("explain", "write")
        # workflow.add_conditional_edges(start_key='judge',
        #                                condition=should_continue2,
        #                                conditional_edge_mapping={"derive": "derive", "analyze": "analyze"})
        # workflow.add_conditional_edges(start_key='analyze',
        #                                condition=should_continue3,
        #                                conditional_edge_mapping={"compute": "compute", "think": "think"})
        workflow.add_edge("write", "design")

        # set up start and end nodes
        workflow.set_entry_point("input_check")
        workflow.set_finish_point("design")

        # compile the graph
        chain = workflow.compile()

        # Execute the graph for each query in parallel
        with ThreadPoolExecutor() as executor:
            parallel_results = list(
                executor.map(
                    lambda q: chain.invoke({"problem": q}, {"recursion_limit": 100}),
                    queries,
                )
            )
        newspaper_html = editor_agent.run(parallel_results)
        newspaper_path = publisher_agent.run(newspaper_html)
        return newspaper_path


if __name__ == "__main__":
    from dotenv import load_dotenv, find_dotenv

    load_dotenv(find_dotenv())
    problem = ["可以介绍一下圆锥曲线吗"]
    master_agent = MasterAgent()
    explanatory_article = master_agent.run(problem)

