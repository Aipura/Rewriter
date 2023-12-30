from src.template import rewrite_prompt_template
from src.config import Config
import os
import platform
from langchain.llms import OpenAI
from src.requests_API import GPT4_requests

# 读取配置
config_instance = Config("config.ini", "dev")

config = config_instance.get_config()

paper_path = config['paper']

def read_file_contents(file_path):
    with open(file_path, 'r', encoding='utf8') as file:
        content = file.read()
    return content

# 读取文件内容
paper = read_file_contents(paper_path)

# 机器人名字
name = config['name']

print(name)
# 格式化模板
rewrite_prompt = rewrite_prompt_template.format(
    name=name,
    cj=config['cj'],
    field=config['field'],
    topic=config['topic'],
    paper=paper,
    language=config['language'],
)

os_name = platform.system()
clear_command = 'cls' if os_name == 'Windows' else 'clear'

# ChatGPT Config
openai_key = "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"
os.environ["OPENAI_API_KEY"] = openai_key
llm = OpenAI(temperature=1)

def build_prompt(history, recent_query):
    prompt = ""
    for query, response in history:
        prompt += f"\n\nUser：{query}"
        prompt += f"\n\n{name}: \n{response}"
    prompt += f"\n\nUser：{recent_query}"
    return prompt


def signal_handler(signal, frame):
    global stop_stream
    stop_stream = True


def main():
    history = []
    print("欢迎使用 GPT4.0 模型，输入内容即可进行对话，clear 清空对话历史，stop 终止程序")
    turn = 0
    while True:
        if turn == 0:
            query = rewrite_prompt
        else:
            query = input("\nUser：")
        if query.strip() == "stop":
            break
        if query.strip() == "clear":
            past_key_values, history = None, []
            os.system(clear_command)
            print("欢迎使用 GPT4.0 模型，输入内容即可进行对话，clear 清空对话历史，stop 终止程序")
            continue
        print(f"\n{name}: \n", end="")
        response = llm(build_prompt(history, query))
        # response = GPT4_requests(build_prompt(history, query))
        print(response, end="", flush=False)
        history.append((query, response))
        turn += 1


if __name__ == "__main__":
    main()
