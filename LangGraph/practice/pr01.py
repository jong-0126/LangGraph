from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from operator import add

class State(TypedDict):
    text: str
    output: str
    log: Annotated[list[str], add]

# 라우터 기능 추가
def router_node(state: State) -> str:
    
    text = state['text']

    if text.startswith('upper '):
        return "upper"
    elif state['text'].startswith('mark '):
        return "mark"
    return "end"

# text output으로 복사
def echo_node(state: State) -> dict:

    text = state['text']

    if text.startswith('upper '):
        text = text[6: ]
    elif text.startswith('mark '):
        text = text[5: ]
    
    return {
        "output": text,
        "log": [f"text: {text}", f"echo done"]
    }

# 대문자로 변경
def upper_node(state:State) -> dict:
    return {
        "output": state["output"].upper(),
        "log": [f"text: {state['text']}", f"upper done"]
    }

# ! 추가
def mark_node(state: State) -> dict:
    return {
        "output": state["output"] + "!",
        "log": [f"text: {state['text']}", f"mark done"]
    }

builder = StateGraph(State)


builder.add_node("echo", echo_node)
builder.add_node("upper", upper_node)
builder.add_node("mark", mark_node)
builder.add_edge(START, "echo")
builder.add_conditional_edges(
    "echo",
    router_node, 
    {"upper":"upper", "mark":"mark","end":END} 
)
builder.add_edge("upper", END)
builder.add_edge("mark", END)

graph = builder.compile()
print(graph.invoke({"text":"hello", "log": []}))
print(graph.invoke({"text":"upper hello", "log": []}))
print(graph.invoke({"text":"mark hello", "log": []}))

