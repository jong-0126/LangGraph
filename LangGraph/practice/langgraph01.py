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
    # re.search() 는 문자열 중간에 어디든 맞는 부분이 있으면 OK
    m = re.search(r"\d+\s*[\+\-\*/]\s*\d+", text)

    if m:
        # m.group는 매치된 결과 계산식만 추출
        state["plan"] = {"next_action": "tool", "expr": m.group(0)}
    else:
        state["plan"] = {"next_action": "final"}

    return state


def tool_node(state: State) -> State:
    # plan이 tool이면 계산, 아니면 그냥 통과
    if state.get("plan", {}).get("next_action") != "tool":
        return state

    # 계산식을 expr에 저장
    expr = state["plan"]["expr"]

    # re.fullmatch() 문자열 전체가 패턴과 정확히 일치해야 OK
    if not re.fullmatch(r"[0-9\+\-\*/\s\.]+", expr):
        state["tool_result"] = "INVALID_EXPR"
        return state

    #eval()은 문자열을 파이썬 코드로 실행해서 결과 리턴
    state["tool_result"] = str(eval(expr))
    return state


def final_node(state: State) -> State:
    if state.get("plan", {}).get("next_action") == "tool":
        state["final"] = f"{state['plan']['expr']} = {state.get('tool_result')}"
    else:
        state["final"] = f"도구 없이 처리: {state.get('input_text','')}"

    return state


# ---- 그래프 구성(직선) ----
g = StateGraph(State)

g.add_node("plan", plan_node)
g.add_node("tool", tool_node)
g.add_node("final", final_node)

g.add_edge(START, "plan")
g.add_edge("plan", "tool")
g.add_edge("tool", "final")
g.add_edge("final", END)

app = g.compile()

print(app.invoke({"input_text": "2+2는 뭐야?"})["final"])
print(app.invoke({"input_text": "안녕"})["final"])
