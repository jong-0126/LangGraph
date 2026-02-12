import re
from typing_extensions import TypedDict
from typing import Dict, Any, Optional

from langgraph.graph import StateGraph, START, END


class State(TypedDict, total=False):
    input_text: str
    plan: Dict[str, Any]
    tool_result: Optional[str]
    final: Optional[str]


def plan_node(state: State) -> State:
    text = state.get("input_text", "")
    m = re.search(r"\d+\s*[\+\-\*/]\s*\d+", text)
    if m:
        state["plan"] = {"next_action": "tool", "expr": m.group(0)}
    else:
        state["plan"] = {"next_action": "final"}
    return state


def tool_node(state: State) -> State:
    expr = state["plan"]["expr"]
    if not re.fullmatch(r"[0-9\+\-\*/\s\.]+", expr):
        state["tool_result"] = "INVALID_EXPR"
        return state
    state["tool_result"] = str(eval(expr))
    return state


def final_node(state: State) -> State:
    if state.get("plan", {}).get("next_action") == "tool":
        state["final"] = f"{state['plan']['expr']} = {state.get('tool_result')}"
    else:
        state["final"] = f"도구 없이 처리: {state.get('input_text','')}"
    return state


# ✅ 라우터: plan 결과를 보고 다음 노드를 정함
def route_after_plan(state: State) -> str:
    action = state.get("plan", {}).get("next_action")
    if action == "tool":
        return "tool"
    return "final"


g = StateGraph(State)
g.add_node("plan", plan_node)
g.add_node("tool", tool_node)
g.add_node("final", final_node)

g.add_edge(START, "plan")

# ✅ 조건 분기(딱 1개)
g.add_conditional_edges(
    "plan",
    route_after_plan,
    {
        "tool": "tool",
        "final": "final",
    }
)

# tool을 탔으면 final로
g.add_edge("tool", "final")
g.add_edge("final", END)

app = g.compile()

print(app.invoke({"input_text": "2+2는 뭐야?"})["final"])
print(app.invoke({"input_text": "안녕"})["final"])
