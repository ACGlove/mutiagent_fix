from tavily import TavilyClient
from dotenv import load_dotenv
from pydantic import BaseModel,Field
from langchain_core.tools import tool
import os 
load_dotenv()
class tool_schema(BaseModel):
    '''联网搜索的工具'''
    query:str=Field(description='搜索关键词。写成直接丢进搜索引擎的短查询：保留关键实体（人名/产品名/版本号/机构名/地名）和限定词（时间、地区、范围、对比项等），不要写成一句完整的问句，也不要把用户原话或任务描述整段抄进来。一个查询只覆盖一个角度；需要多个角度的信息时，换一组关键词再调用一次，不要把大量不相关的词堆进同一个很长的查询里。')


@tool(args_schema=tool_schema)
def search(query:str):
    '''联网搜索工具：检索实时网页，返回标题、链接和内容摘要。

    何时该用：
    - 需要可能已过时或本来就不掌握的客观信息：最新进展、具体数据与统计、日期、版本号、价格、政策或新闻事件；
    - 遇到不熟悉或不确定的概念、缩写、产品名、人名、机构名，需要先弄清它是什么；
    - 需要给出可以核查的来源链接时。

    何时不要用：
    - 纯常识、纯推理、写作润色、代码或数学推导类问题，凭已有知识就能回答的；
    - 同一组或高度相近的关键词已经搜过并拿到了结果，不要重复调用，直接基于已有结果作答；
    - 目标已经由前面的步骤查清、或当前步骤并不需要外部事实时。

    返回：多条搜索结果的标题、链接与内容摘要。引用时请保留链接，不要大段照抄原文。'''
    tavily=TavilyClient(api_key=os.getenv('TAVILY_API_KEY'))
    try:
        response=tavily.search(
                query,
                max_results=5,
                search_depth="advanced"
            )['results']
    except TimeoutError as f:
        return f'超时错误,错误信息为{f},请重新调用工具'
    res='\n'
    for i in response:
        res+=f'标题:{i['title']},链接:{i['url']},内容:{i['content']}'
    return res



