import os
from pathlib import Path

from langchain_core.tools import tool
from pydantic import BaseModel,Field


class write_file_schema(BaseModel):
    '''写入文件的入参'''
    path:str=Field(description='要写入的文件路径。可以用相对路径（相对当前工作目录）或绝对路径；父目录不存在时会自动创建。例如 output/report.md。')
    content:str=Field(description='要写入文件的完整文本内容，会按原样写入（不转义、不追加）。')


@tool(args_schema=write_file_schema)
def write_file(path:str,content:str):
    '''把文本写入文件：用于把结果落盘为 .md、.txt、.json、代码等文本文件。

    何时该用：
    - 需要把最终答复、汇总报告或中间产物保存成文件时；
    - 需要生成代码、配置、JSON 等文本文件时。

    注意：
    - 会覆盖同名文件的原有内容（不是追加），要保留旧内容就先自己想清楚再写；
    - 内容按原样写入，编码固定为 UTF-8，换行按 LF 原样写入；
    - 一次调用只写一个文件，内容必须完整给出；
    - 本工具只负责写文件，不能读取、追加、删除或列目录。

    返回：成功时返回写入文件的绝对路径和字符数；失败时返回错误原因。'''
    file_path=Path(os.path.expanduser(path))
    try:
        file_path.parent.mkdir(parents=True,exist_ok=True)
        file_path.write_text(content,encoding='utf-8',newline='')
    except OSError as f:
        return f'写入失败:文件{file_path},错误信息为{f},请检查路径后重新调用'
    return f'写入成功:文件{file_path.resolve()},共{len(content)}个字符'
