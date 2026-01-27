from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class CounterState(TypedDict):
    count: int

def first_increment(state):
    print("첫 번째 증가")
    return {"count": state["count"] + 1}

def second_increment(state):
    print("두 번째 증가")
    return {"count": state["count"] + 10}

graph = StateGraph(CounterState)
graph.add_node("first", first_increment)
graph.add_node("second", second_increment)

graph.add_edge(START, "first")
graph.add_edge("first", "second")
graph.add_edge("second", END)

app = graph.compile()
result = app.invoke({"count":0})
print(f"최종 결과: {result}")