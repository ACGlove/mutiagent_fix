from langchain_core.messages import SystemMessage,HumanMessage



def structured_node(model,prompt):
    def output(state):
        messages=[SystemMessage(prompt)]+[HumanMessage(state['goal'])]
        result=model.invoke(messages)
        return {
            'structured_output':result
        }
    return output




def llm_call(prompt,model):
    def llm(state):
        msg=state.get('messages') or [HumanMessage(state['subtask'])]   #如messages未填入消息，则说明为第一次调用，输入子任务
        result=model.invoke([SystemMessage(prompt)]+msg)         
        return {
            'messages':[result]            #只传list+list

        }
    return llm
    





















