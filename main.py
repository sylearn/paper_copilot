from src.agent import Agent
from src.vector_indexer import VectorIndexer
from termcolor import colored
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit import prompt
import os

def start():
    print(colored("命令:", "cyan"))
    print(colored("-"*50, "cyan"))
    commands = {
        "/create": "创建知识库",
        "/chat": "基于知识库问答（后接问题）",
        "/save_chat_history": "保存聊天记录",
        "/clear_chat_history": "清除聊天记录",
        "/load_chat_history": "加载聊天记录",
        "/quit": "退出程序",
        "/save_last_response": "保存上一次的回答为markdown文件",
        "/help": "显示帮助信息"
    }
    command_list = list(commands.keys())
    for cmd, desc in commands.items():
        print(f"{colored(cmd, 'magenta'):<10} {colored(desc, 'dark_grey')}")
    completer = WordCompleter(
            command_list)
    #初始化agent
    agent = Agent(prompt_path="src/prompt/文献分析助手.md",model="o1-mini",top_n=8,relation_threshold=0.1)
    while True:
        #显示当前知识库
        print("-"*50)
        print("-"*50)
        command = prompt("\nYou:\n" + " ", completer=completer).strip()
        if command.startswith("/quit"):
            break
        elif command.startswith("/save_last_response"):
            agent.save_last_response()
        elif command.startswith("/create"):
            #操作数据库
            database_path = os.getenv("DATABASE_PATH")
            #初始化向量数据库
            vector_indexer = VectorIndexer(database_path=database_path)
            vector_indexer.load_index()
            vector_indexer.show_table_info()
        elif command.startswith("/save_chat_history"):
            agent.save_chat_history()
        elif command.startswith("/clear_chat_history"):
            agent.clear_chat_history()
        elif command.startswith("/load_chat_history"):
            agent.load_chat_history()
        elif command.startswith("/chat"):
            #这是基于向量数据库的问答
            agent.chat_with_vector_database(command[6:])
        elif command.startswith("/help"):
            print(colored("命令:", "cyan"))
            print(colored("-"*50, "cyan"))
            for cmd, desc in commands.items():
                print(f"{colored(cmd, 'magenta'):<10} {colored(desc, 'dark_grey')}")
        else:
            #不加载知识库，直接问答
            agent.chat_with_ai(command)
if __name__ == "__main__":
    start()

