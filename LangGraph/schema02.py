# 명시적 입출력 스키마
# 입력과 출력을 별도로 정의하여 인터페이스를 명확하게 제어합니다.
# API 같은 명환한 인터페이스가 필요한 경우
# 외부 시스템과 연동할 때
# 내부 처리 과정을 숨기고 싶을 때

from typing_extensions import TypedDict
from typing import Annotated
from operator import add

class InputState(TypedDict):
    question: str

class OutputState(TypedDict):
    answer: str

class OverallState(InputState, OutputState):
    intermediate_data: str
    search_results: list[str]

def search_node(state: InputState) -> dict:
    return {
        "search_results" : ["결과1", "결과2"],
        "intermediate_data": f"'{state['question']}' 검색완료" 
    }

def answer_node(state: OverallState) -> OutputState:
    return{"answer": f"검색결과 :{state['search_results'][0]}"}
