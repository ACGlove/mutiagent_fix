from .graph import Planner
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from .prompt import PLANNER_PROMPT
load_dotenv()
model_name=os.getenv('LLM_MODEL')
baseurl=os.getenv('LLM_BASE_URL')
apikey=os.getenv('LLM_API_KEY')

model=ChatOpenAI(
    base_url=baseurl,
    model=model_name,
    api_key=apikey
)



def build_planner_node(state):
    planner=Planner(model=model,prompt=PLANNER_PROMPT)   #compile后的对象invoke传入state字典
    result=planner.graph.invoke({
        'goal':state['goal']
    })                    #返回的是dict
    plan=[p.model_dump(mode='json') for p in result['structured_output'].plan]
    return {
        'plan':plan,
        'subtask_index':0,        #归零游标，防止checkpointer持久化上一次的index
        'step_result':[]

    }

