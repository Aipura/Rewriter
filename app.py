import gradio as gr
import os
import time
import shutil
import codecs

# Chatimport shutilbot demo with multimodal input (text, markdown, LaTeX, code blocks, image, audio, & video). Plus shows support for streaming text.
from src.template import rewrite_prompt_template
from src.config import Config
import os
import platform
from langchain.llms import OpenAI
from src.requests_API import GPT4_requests

with gr.Blocks() as demo:
    bot_name = gr.State(value="Rewriter")
    paper_path = gr.State(value="")
    file_dir = gr.State(value="files")
    public_file_dir = gr.State(value="")


    def build_prompt(history, name, mode="chat"):
        prompt = ""
        for query, response in history[:-1]:
            prompt += f"\n\nUser：{query}"
            prompt += f"\n\n{name}: \n{response}"
        if mode == "download":
            prompt += f"\n\nUser：{history[-1][0]}"
            prompt += f"\n\n{name}: \n{history[-1][1]}"
        else:
            prompt += f"\n\nUser：{history[-1][0]}"
        return prompt


    def print_like_dislike(x: gr.LikeData):
        print(x.index, x.value, x.liked)


    def read_file_contents(file_path):
        with open(file_path, 'r', encoding='utf8') as file:
            content = file.read()
        return content


    def add_text(history, text, name, cj, field, topic, language, paper_path):
        if text:
            if not history:
                if not paper_path:
                    gr.Warning("Paper file not found.")
                    return [], gr.Textbox(value="", interactive=True,
                                          placeholder="Enter text and press enter, or press submit button", )
                bot_name = name
                # 读取文件内容
                paper = read_file_contents(paper_path)
                # 格式化模板
                rewrite_prompt = rewrite_prompt_template.format(
                    name=name,
                    cj=cj,
                    field=field,
                    topic=topic,
                    language=language,
                    paper=paper
                )
                query = rewrite_prompt + text
            else:
                query = text
            history = history + [[query, None]]
        return history, gr.Textbox(value="", interactive=False), gr.Button(value="Submit",
                                                                           interactive=False), gr.Button(value="Reset",
                                                                                                         interactive=False)


    def bot(history, name, openai_key, temperature):
        if history:
            # print(history)
            prompt = build_prompt(history, name)
            os.environ["OPENAI_API_KEY"] = openai_key
            llm = OpenAI(temperature=temperature)
            response = llm(prompt)
            # response = GPT4_requests(prompt)
            history[-1][1] = response
        return history


    def add_file(history, file):
        history = history + [((file.name,), None)]
        return history


    def upload_file(file_obj, file_dir):
        print(file_obj.name)
        public_file_dir = os.path.dirname(file_obj.name)
        print(file_dir)
        # 将文件复制到目标目录
        shutil.copy(file_obj.name, file_dir)
        # 获取上传Gradio的文件名称
        FileName = os.path.basename(file_obj.name)
        # 获取拷贝在临时目录的新的文件地址
        NewfilePath = os.path.join(file_dir, FileName)
        paper_path = NewfilePath
        print(paper_path)
        return paper_path, public_file_dir, gr.Button(value="下载", visible=True)


    def download_file(history, file_dir, paper_path, name):
        if not history:
            gr.Warning("Polished contents not found.")
            return
        print(paper_path)
        new_name = "rewrited_" + os.path.basename(paper_path)
        file_path = os.path.join(file_dir, new_name)
        with codecs.open(file_path, "w", encoding="utf-8") as file:
            file.write(build_prompt(history, name, mode="download"))
        # gr.Info("Click on the download link for the polished file.")
        return gr.Textbox(
            label="下载链接",
            info="复制文件路径拼接到服务器地址后得到完整下载地址",
            lines=1,
            visible=True,
            value="/file=" + file_path,
            interactive=False
        )


    def reset_state():
        return gr.Textbox(value="", interactive=True), gr.Button(value="Submit", interactive=True), gr.Button(
            value="Reset", interactive=True)


    def reset():
        return [], None


    chatbot = gr.Chatbot(
        [],
        elem_id="Rewriter",
        bubble_full_width=False,
        height=666,
        avatar_images=(None, (os.path.join("images", "avatar.png"))),
    )
    with gr.Column():
        with gr.Row():
            txt = gr.Textbox(
                scale=4,
                show_label=False,
                placeholder="Enter text and press enter, or press submit button",
                container=False,
            )
            btn_submit = gr.Button(value="Submit")
            btn_reset = gr.Button(value="Reset")

        name_element = gr.Textbox(
            label="机器人名字",
            info="",
            lines=1,
            value="Academic Paper Rewriting Expert",
        ),
        openai_key_element = gr.Textbox(
            label="OpenAI Key",
            info="",
            lines=1,
            value="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",
        ),
        temperature_element = gr.Slider(0, 1, value=1, label="Temperature", info="Choose between 0 and 1"),
        cj_element = gr.Textbox(
            label="目标会议/期刊",
            info="",
            lines=1,
            value="ACL Conference",
        ),
        field_element = gr.Textbox(
            label="研究领域",
            info="",
            lines=1,
            value="LLM",
        ),
        topic_element = gr.Textbox(
            label="研究主题",
            info="",
            lines=1,
            value="Multi-Agent",
        ),
        language_element = gr.Textbox(
            label="语言",
            info="",
            lines=1,
            value="English",
        ),
        paper_element = gr.File(file_types=["txt"], label="论文")

        download_btn = gr.Button(value="下载", visible=False),
        download_element = gr.Textbox(
            label="下载链接",
            info="",
            lines=1,
            visible=False,
            value="",
        )

    # txt_msg = txt.submit(add_text, [chatbot, txt, name_element[0], cj_element[0], field_element[0], topic_element[0]],
    #                      [chatbot, txt], queue=False).then(
    #     bot, chatbot, chatbot, api_name="bot_response"
    # )

    # btn_msg = btn.click(add_text, [chatbot, txt, name_element[0], cj_element[0], field_element[0], topic_element[0]],
    #                      [chatbot, txt, name_element[0]], queue=False).then(
    #     bot, chatbot, chatbot, api_name="bot_response"
    # )

    # btn_msg.then(lambda: gr.Textbox(interactive=True), None, [txt], queue=False)
    txt_msg = txt.submit(add_text, [
        chatbot,
        txt,
        name_element[0],
        cj_element[0],
        field_element[0],
        topic_element[0],
        language_element[0],
        paper_path
    ], [chatbot, txt, btn_submit, btn_reset]).then(bot, [
        chatbot,
        name_element[0],
        openai_key_element[0],
        temperature_element[0]
    ], [
                                                       chatbot
                                                   ], api_name="bot_response")

    txt_msg.then(reset_state, None, [txt, btn_submit, btn_reset])

    btn_msg = btn_submit.click(add_text, [
        chatbot,
        txt,
        name_element[0],
        cj_element[0],
        field_element[0],
        topic_element[0],
        language_element[0],
        paper_path
    ], [chatbot, txt, btn_submit, btn_reset]).then(bot, [
        chatbot,
        name_element[0],
        openai_key_element[0],
        temperature_element[0]
    ], [
                                                       chatbot
                                                   ], api_name="bot_response")

    btn_msg.then(reset_state, None, [txt, btn_submit, btn_reset])

    btn_reset.click(reset, None, [chatbot, paper_element])

    paper_element.upload(upload_file, [paper_element, file_dir], [paper_path, public_file_dir, download_btn[0]])

    download_btn[0].click(download_file, [chatbot, public_file_dir, paper_path, bot_name], [download_element])

    chatbot.like(print_like_dislike, None, None)

demo.queue()
demo.launch(
    share=False,
    server_port=6006,
    debug=False
)