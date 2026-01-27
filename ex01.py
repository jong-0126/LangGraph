from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class MyState(TypedDict):
    message:str

def say_hello(state):
    return {"message": "Hello, LangGraph!"}

graph = StateGraph(MyState)
graph.add_node("hello", say_hello)
graph.add_edge(START, "hello")
graph.add_edge("hello", END)

app = graph.compile()
result = app.invoke({"message": ""})
print(result)