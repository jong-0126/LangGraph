# 다중 스키마 + PrivateState

# RAG 파이프라인
# 다단계 처리가 필요한 복잡한 시스템
# 각 단계별로 다른 데이터 구조가 필요한 경우
from typing_extensions import TypedDict

class OverallState(TypedDict):
    question: str
    answer: str

class PrivateState(TypedDict):
    internal_score: float
    debug_info: str

def internal_node(state: OverallState) -> PrivateState:
    # 노드는 OverallState에 정의되지 않은 필드도 반환 가능
    return {
        "internal_score": 0.95,
        "debug_info": "내부 처리 완료"
    }