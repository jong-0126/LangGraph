# 기본 스키마
# 입력과 출력이 동일한 단일 스키마를 사용하는 가장 기본적인 형태
# 간단한 Q&A 시스템 
# 상태가 복잡하지 않은 선형적 워크플로우
# 프로토타이핑이나 학습 목적

from typing_extensions import TypedDict
from typing import Annotated
from operator import add

class BasicState(TypedDict):
    user_input: str
    ai_response: str
    conversation_history: Annotated[list[str], add]

def chatbot_node(state: BasicState) -> dict:
    response = f"'{state['user_input']}'에 대한 응답입니다."
    return{
        "ai_response": response,
        "conversation_history": [f"User: {state['user_input']}",f"AI: {response}"]
    }