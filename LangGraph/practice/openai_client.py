from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_openai import ChatOpenAI

load_dotenv()

gemini = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.7
)

# gpt4_mini = ChatOpenAI(
#     model = "gpt-4.1-mini",
#     temperature = 0.7,
#     max_tokens = 150
# )

# gpt4 = ChatOpenAI(
#     model = "gpt-4.1",
#     temperature = 0.7,
#     max_tokens = 300
# )