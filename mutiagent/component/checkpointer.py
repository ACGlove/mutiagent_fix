"""Checkpointer（状态持久化）工厂。

用法（只在主图的编译处注入一次）：
    from ..component.checkpointer import build_checkpointer
    self.checkpointer = checkpointer or build_checkpointer()
    self.graph = graph.compile(checkpointer=self.checkpointer)

为什么单独放一个文件：
- saver 属于"持久化"这一层的基础设施，和 node.py / edge.py 一样是搭图的零件；
- 必须由调用方（组合根）建一次再注入。不要在 Agent.__init__ 里每次 new 一个
  InMemorySaver，否则每次请求都是全新的空记忆，checkpoint 形同虚设；
- 用哪种后端由 .env 的 GRAPH_CHECKPOINTER 决定，开发/测试可替换。

后端取值（不区分大小写）：
- memory / inmemory  -> langgraph.checkpoint.memory.InMemorySaver（进程内有效，默认）
- sqlite             -> langgraph.checkpoint.sqlite.SqliteSaver，落盘到 <项目根>/memory/checkpoint.db
"""
import os
import sqlite3
from pathlib import Path

from dotenv import load_dotenv
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()

# 本文件位于 <项目根>/mutiagent/component/ 下，parents[2] 就是项目根（mutiagent_fix）。
# 数据库放在包外面，避免把运行时数据混进可导入的包里。
DB_PATH = Path(__file__).resolve().parents[2] / 'memory' / 'checkpoint.db'


def build_checkpointer(kind: str | None = None):
    """按 .env 的 GRAPH_CHECKPOINTER 造一个长生命周期的 saver，进程内只调用一次。"""
    kind = (kind or os.getenv('GRAPH_CHECKPOINTER') or 'memory').strip().lower()

    if kind in ('memory', 'inmemory'):
        return InMemorySaver()

    if kind == 'sqlite':
        from langgraph.checkpoint.sqlite import SqliteSaver
        DB_PATH.parent.mkdir(parents=True, exist_ok=True)
        # 注意：SqliteSaver.from_conn_string 是 contextmanager，出了 with 块连接就关了，
        # 不适合"返回一个长生命周期 saver"的用法，所以这里自己建长连接。
        conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
        return SqliteSaver(conn)

    raise ValueError(f'不支持的 GRAPH_CHECKPOINTER 取值: {kind}（可选 memory / sqlite）')
