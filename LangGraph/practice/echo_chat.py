from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver

class State(TypedDict):
    messages: Annotated[list, add_messages]

def route(state: State) -> str:
    last = state["messages"][-1]
    text = last.content

    if isinstance(last, HumanMessage) and text.startswith("/calc "):
        return 'tools'
    if isinstance(last, HumanMessage):
        return 'chat'
    return 'end'

def chat_node(state: State) -> dict:
    last = state['messages'][-1]
    if last.content.startswith('[tool]'):
        result = last.content.split('=')[1].strip()
        reply = AIMessage(content=f"계산 결과는 {result}입니다.")
        return {"messages": [reply]}
        
    reply = AIMessage(content=f"너는 '{last.content}'라고 했어.")
    return {"messages": [reply]}


def tools_node(state: State) -> dict:
    text = state["messages"][-1].content
    expr = text[len("/calc "):]
    a, b = expr.split("+")
    result = int(a.strip()) + int(b.strip())

    return {"messages": [AIMessage(content=f"[tool] {expr} = {result}")]}

builder = StateGraph(State)

builder.add_node("chat", chat_node)
builder.add_node("tools", tools_node)
builder.add_conditional_edges(START, route, {"tools": "tools", "chat": "chat", "end": END})
builder.add_edge("tools", "chat")
builder.add_conditional_edges("chat", route, {"tools": "tools", "chat": "chat", "end": END})

checkpointer = InMemorySaver()

graph = builder.compile(checkpointer = checkpointer)
config = {"configurable": {"thread_id": "user-1"}}

r1 = graph.invoke({"messages": [HumanMessage(content="안녕")]}, config=config)
print(len(r1["messages"]))

r2 = graph.invoke({"messages": [HumanMessage(content="방금 뭐라고 했지?")]}, config=config)
print(len(r2['messages']))

r3 = graph.invoke({"messages": [HumanMessage(content="/calc 2+3")]}, config=config)
print(r3["messages"])