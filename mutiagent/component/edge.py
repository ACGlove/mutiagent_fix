
from langgraph.graph import END




def is_tool_use(state):
    if state['messages'][-1].tool_calls:
        return 'tool'
    else:
        return END


def is_subtask_finish(state):
    if state['subtask_index']==len(state['plan']):
        return 'reporter'
    else:
        return 'executor'






















