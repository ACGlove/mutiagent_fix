import os
from langgraph.graph import StateGraph,START



from ..schema.state import Graph_state

from ..agent.planner.build import build_planner_node
from ..agent.executor.build import build_executor_node
from ..agent.reporter.build import build_reporter_node
from ..component.checkpointer import build_checkpointer
from ..component.edge import is_subtask_finish



class Agent:
    def __init__(self,checkpointer=None):
        graph=StateGraph(Graph_state)
        graph.add_node('planner',build_planner_node)
        graph.add_node('executor',build_executor_node)
        graph.add_node('reporter',build_reporter_node)

        graph.add_edge(START,'planner')
        graph.add_edge('planner','executor')
        graph.add_conditional_edges(
            'executor',
            is_subtask_finish
        )



        # saver 由调用方（组合根）建一次并注入；不传就按 .env 的 GRAPH_CHECKPOINTER 新建
        self.checkpointer=checkpointer or build_checkpointer()
        self.graph=graph.compile(checkpointer=self.checkpointer)


    def __call__(self,goal,thread_id=None):
        thread_id=thread_id or os.getenv('GRAPH_THREAD_ID') or 'default-thread'
        result=self.graph.invoke(
            {
                'goal':goal                #往invoke里传入state字段的初始值，会写入state
            },
            config={
                'configurable':{'thread_id':thread_id},      #带 checkpointer 时 thread_id 必填
                'recursion_limit':int(os.getenv('GRAPH_RECURSION_LIMIT',50))
            }
        )
        return result['result']              #compile的对象invoke返回state里有值的键值对
                                                  
        













































