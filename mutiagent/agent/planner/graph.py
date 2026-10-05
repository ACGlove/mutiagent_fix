from langgraph.graph import StateGraph,START

from ...component.node import structured_node
from ...schema.structured_schema import Plan
from ...schema.state import Planner_state


class Planner:
    def __init__(self,model,prompt):
        # ChatOpenAI 的 with_structured_output 默认 method="json_schema"，会发 response_format，
        # 而 DeepSeek 不支持这种 Structured Outputs，必须显式用 function_calling（走 tools）
        self.model=model.with_structured_output(Plan,method='function_calling')
        graph=StateGraph(Planner_state)
        graph.add_node('llm',structured_node(model=self.model,prompt=prompt))
        graph.add_edge(START,'llm')
        self.graph=graph.compile(name='planner')








    







































