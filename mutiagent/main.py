from .graph.graph import Agent
ag=Agent()
def agent_call(goal,id):
    
    result=ag(goal=goal,thread_id=id)
    return result



if __name__=='__main__':
    print(agent_call(goal=r'帮我查今年哔站热度最好的三部番，再将相关信息写入mutiagent\a.txt',id=1))





