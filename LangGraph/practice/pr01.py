from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    text: str
    output: str

def echo_node(state: State) -> dict:
    return {"output": state["text"]}

def upper_node(state:State) -> dict:
    return {"output": state["output"].upper()}

def mark_node(state: State) -> dict:
    return {"output": state["output"] + "!"}

builder = StateGraph(State)


builder.add_node("echo", echo_node)
builder.add_node("upper", upper_node)
builder.add_node("mark", mark_node)

builder.add_edge(START, "echo")
builder.add_edge("echo", "upper")
builder.add_edge("upper", "mark")
builder.add_edge("mark", END)

graph = builder.compile()
print(graph.invoke({"text":"hello"}))



