from typing_extensions import TypedDict
from typing import Annotated
from langgraph.graph.message import add_messages
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.tools import tool
from openai_client import gemini

class State(TypedDict):
    messages: Annotated[list, add_messages]


# LLM이 도구로 인식함 @tool이 붙은 함수는
@tool
def calc(expression: str) -> str:
    """간단 계산기. 예: 2+3, 10-7, 4*5, 8/2 (연산자 1개만 지원)"""
    expr = expression.replace(" ", "")
    for op in ["+", "-", "*", "/"]:
        if op in expr: 
            left, right = expr.split(op, 1)
            a,b = int(left), int(right)
            if op == "+": return str(a+b)
            if op == "-": return str(a-b)
            if op == "*": return str(a*b)
            if op == "/":
                if b == 0: return "ERROR: division by zero"
                return str(a//b)
    return "ERROR: unsupported expression"

tools = [calc]
#gemini.bind_tools를 이용해서 calc 도구를 사용할 수 있도록 설정
llm_with_tools = gemini.bind_tools(tools)


# LLM을 한번 호출하는 그래프 노드
def assistant(state: State) -> dict:
    msg = llm_with_tools.invoke(state["messages"])
    return {"messages": [msg]}

builder = StateGraph(State)

builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "assistant")

builder.add_conditional_edges("assistant", tools_condition, {"tools": "tools", "__end__": END})
builder.add_edge("tools", "assistant")

graph = builder.compile(checkpointer=InMemorySaver())

config = {"configurable":{"thread_id":"user-1"}}

print(graph.invoke({"messages":[HumanMessage(content="2+3 계산해줘")]}, config=config)["messages"][-1].content)
print(graph.invoke({"messages":[HumanMessage(content="그럼 10-7도")]}, config=config)["messages"][-1].content)
