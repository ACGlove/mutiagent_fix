from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage,HumanMessage
from .prompt import REPORTER_PROMPT
load_dotenv()
model_name=os.getenv('LLM_MODEL')
baseurl=os.getenv('LLM_BASE_URL')
apikey=os.getenv('LLM_API_KEY')

model=ChatOpenAI(
    base_url=baseurl,
    model=model_name,
    api_key=apikey
)


def build_reporter_node(state):
    step_results=state['step_result']                    #将step_result拼成一起传给汇总者
    block=[]
    for i,p in enumerate(state['plan']):
        res=step_results[i]
        block.append(
        f'步骤目标：{p.get("objective", "")}\n'
        f'预期产出：{p.get("expected_output", "")}\n'
        f'实际结果：\n{res}'
        )
    all_step='\n\n'.join(block)
    result=model.invoke([SystemMessage(REPORTER_PROMPT)]+[HumanMessage(f'任务总目标:{state['goal']}'+f'\n子任务的完成情况如下{all_step}')])
    return {
        'result':result.content
    }
