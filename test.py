from langchain.llms import OpenAI
import os

os.environ["OPENAI_API_KEY"] = "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"
llm = OpenAI(temperature=1)
response = llm("Who are you?")