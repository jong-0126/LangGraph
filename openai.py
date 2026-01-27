from dotenv import load_dotenv
from langchain_openai import ChatOpneAI

load_dotenv()

gpt4_mini = ChatOpneAI(
    model = "gpt-4.1-mini",
    temperature = 0.7,
    max_tokens = 150
)

gpt4 = ChatOpneAI(
    model = "gpt-4.1",
    temperature = 0.7,
    max_tokens = 300
)