import re
from typing_extensions import TypedDict
from typing import Dict, Any, Optional, List

from langgraph.graph import StateGraph, START, END


class State(TypedDict, total=False):
    input_text: str
    plan: Dict[str, Any]
    tool_result: Optional[str]

    # validate 결과
    ok: bool
    errors: List[str]

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

    # 실습용 최소 안전 필터
    if not re.fullmatch(r"[0-9\+\-\*/\s\.]+", expr):
        state["tool_result"] = None
        # tool에서 에러 문자열을 직접 넣지 말고 validate에서 판단하게 해도 됨
        return state

    state["tool_result"] = str(eval(expr))
    return state


def validate_node(state: State) -> State:
    state["errors"] = []
    state["ok"] = True

    action = state.get("plan", {}).get("next_action")

    # tool을 쓰기로 했는데 결과가 없으면 실패
    if action == "tool":
        if state.get("tool_result") is None:
            state["ok"] = False
            state["errors"].append("tool_result가 없습니다(계산 실패 또는 입력이 비정상).")

    if action == 'tool':
        text = state.get("input_text", "")
        if re.search(r"[A-Za-z_;]", text):
            state["ok"] = False
            state["errors"].append("입력에 허용되지 않는 문자가 포함되어 있습니다.")
    
    # plan 자체가 이상한 경우
    if action not in ("tool", "final"):
        state["ok"] = False
        state["errors"].append(f"next_action이 올바르지 않습니다: {action}")

    return state


def final_node(state: State) -> State:
    if not state.get("ok", True):
        # 실패 응답
        errs = " / ".join(state.get("errors", [])) or "알 수 없는 오류"
        state["final"] = f"실패: {errs}"
        return state

    # 성공 응답
    if state.get("plan", {}).get("next_action") == "tool":
        state["final"] = f"{state['plan']['expr']} = {state.get('tool_result')}"
    else:
        state["final"] = f"도구 없이 처리: {state.get('input_text','')}"

    return state


def route_after_plan(state: State) -> str:
    action = state.get("plan", {}).get("next_action")
    return "tool" if action == "tool" else "validate"


g = StateGraph(State)
g.add_node("plan", plan_node)
g.add_node("tool", tool_node)
g.add_node("validate", validate_node)
g.add_node("final", final_node)

g.add_edge(START, "plan")

# plan 이후: tool 갈지 validate로 바로 갈지 분기
g.add_conditional_edges(
    "plan",
    route_after_plan,
    {"tool": "tool", "validate": "validate"}
)

# tool을 했으면 validate로
g.add_edge("tool", "validate")

# validate 후에는 final로
g.add_edge("validate", "final")
g.add_edge("final", END)

app = g.compile()

print(app.invoke({"input_text": "2+2는 뭐야?"})["final"])
print(app.invoke({"input_text": "안녕"})["final"])

# 실패 케이스도 한 번 보자(의도적으로 위험 문자 섞기)
print(app.invoke({"input_text": "10+10; import os"})["final"])
