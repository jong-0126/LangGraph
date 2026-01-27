from langchain_core.messages import HumanMessage
from openai_client import gemini

gemini_response = gemini.invoke("Explain the components of LangGraph.")
print("Gemini's response:", gemini_response)

# response_mini = gpt4_mini.invoke([HumanMessage(content="Hello, how are you?")])
# print(response_mini.content)

# reponse_full = gpt4.invoke([HumanMessage(content="Explain the concept of machine learning.")])
# print(reponse_full.content)
