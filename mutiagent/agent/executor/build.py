from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from .graph import Executor
from .prompt import EXECUTOR_PROMPT
from ...tool.search import search
from ...tool.write_file import write_file




load_dotenv()
model_name=os.getenv('LLM_MODEL')
baseurl=os.getenv('LLM_BASE_URL')
apikey=os.getenv('LLM_API_KEY')

model=ChatOpenAI(
    base_url=baseurl,
    model=model_name,
    api_key=apikey
)

def build_executor_node(state):
    new_model=Executor(model=model,prompt=EXECUTOR_PROMPT,tools=[search,write_file])
    
    index_plan=state.get('subtask_index') or 0
    plan=state['plan'][index_plan]                                  
    subtask=f'''总目标:{state['goal']}
                此步骤id:{plan['id']}
                依赖的步骤id:{plan['step_depends_on']}
                此步骤目标:{plan['objective']}
                预期结果:{plan['expected_output']}
                已完成的步骤结果:{state['step_result']}'''
    step_result=new_model.graph.invoke({'subtask':subtask})  #在子图里读subtask字段，state 属于一次 run,不属于 compile() 出来的那个图对象
    result=[step_result['messages'][-1].content]   #一次invoke算一个state,所以上个循环的messages不会污染下个循环的state

    return {
        'step_result':state['step_result']+result,
        'subtask_index':state.get('subtask_index')+1
    }
