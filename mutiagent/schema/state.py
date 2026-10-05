from typing import Any,TypedDict,List,Annotated
from langchain_core.messages import AnyMessage
import operator

from langgraph.channels import EphemeralValue


class Graph_state(TypedDict):
    goal:str
    step_result:Annotated[List[str], EphemeralValue]    #改为覆写，不进checkpoint持久化
    plan:list[dict]
    result:str
    subtask_index:int   #记录下个子任务的下标




class Planner_state(TypedDict):
    goal:str
    structured_output:Any



class Executor_state(TypedDict):
    messages:Annotated[List[AnyMessage],operator.add]
    # step_result=Annotated[List[str],operator.add]
    subtask:str
    
    









