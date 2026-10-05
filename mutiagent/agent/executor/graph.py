from langgraph.graph import StateGraph,START
from langgraph.prebuilt import ToolNode


from ...schema.state import Executor_state
from ...component.node import llm_call
from ...component.edge import is_tool_use




class Executor:
    def __init__(self,model,prompt,tools:list):
        self.model=model.bind_tools(tools)
        graph=StateGraph(Executor_state)

        graph.add_node('llm',llm_call(model=self.model,prompt=prompt))
        graph.add_node('tool',ToolNode(tools))


        graph.add_edge(START,'llm')
        graph.add_conditional_edges(
            'llm',
            is_tool_use
        )

        graph.add_edge('tool','llm')


        self.graph=graph.compile(name='executor')






















