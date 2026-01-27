from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

gpt4_mini = ChatOpenAI(
    model = "gpt-4.1-mini",
    temperature = 0.7,
    max_tokens = 150
)

gpt4 = ChatOpenAI(
    model = "gpt-4.1",
    temperature = 0.7,
    max_tokens = 300
)