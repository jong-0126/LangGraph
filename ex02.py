from langgraph.graph import StateGraph, START, END
from typing import TypedDict

class CounterState(TypedDict):
    count: int

def increment(state):
    print(f"현재 카운트: {state['count']}")
    new_count = state["count"] + 1
    print(f"새로운 카운트: {new_count}")
    return {"count": new_count}

graph = StateGraph(CounterState)
graph.add_node("increment", increment)
graph.add_edge(START, "increment")
graph.add_edge("increment", END)

app = graph.compile()
result = app.invoke({"count": 0})
print(f"최종 결과: {result}")