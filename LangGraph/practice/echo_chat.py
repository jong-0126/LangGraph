from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    messages: Annotated[list, add_messages]


def chat_node(state: State) -> dict:
    last = state['messages'][-1]
    reply = AIMessage(content=f"너는 '{last.content}'라고 했어.")
    return {"messages": [reply]}

builder = StateGraph(State)
builder.add_node("chat", chat_node)
builder.add_edge(START, "chat")
builder.add_edge("chat", END)

graph = builder.compile()

result = graph.invoke({"messages": [HumanMessage(content="안녕")]})
print(result["messages"])