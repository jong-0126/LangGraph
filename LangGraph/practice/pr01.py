from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from operator import add

class State(TypedDict):
    text: str
    output: str
    log: Annotated[list[str], add]

# text output으로 복사
def echo_node(state: State) -> dict:
    return {
        "output": state["text"],
        "log": [f"text: {state['text']}", f"echo done"]
    }

# 대문자로 변경
def upper_node(state:State) -> dict:
    return {
        "output": state["output"].upper(),
        "log": [f"text: {state['output']}", f"upper done"]
    }

# ! 추가
def mark_node(state: State) -> dict:
    return {
        "output": state["output"] + "!",
        "log": [f"text: {state['output']}", f"mark done"]
    }

builder = StateGraph(State)


builder.add_node("echo", echo_node)
builder.add_node("upper", upper_node)
builder.add_node("mark", mark_node)

builder.add_edge(START, "echo")
builder.add_edge("echo", "upper")
builder.add_edge("upper", "mark")
builder.add_edge("mark", END)

graph = builder.compile()
print(graph.invoke({"text":"hello", "log": []}))



