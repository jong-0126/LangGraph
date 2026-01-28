from langgraph.graph import StateGraph, START, END
from typing import TypedDict

# 데이터 저장소 만들기
class MyState(TypedDict): #MyState는 데이터 저장소
    message:str # message라는 문자열 저장

# 작업 함수 만들기
def say_hello(state): # say_hello는 실제 작업을 하는 함수
    return {"message": "Hello, LangGraph!"} # 현재 상태(state)에 따라서 새로운 상태를 돌려준다

# 그래프 만들기
graph = StateGraph(MyState) # 데이터 저장소를 사용하는 그래프를 만든다
graph.add_node("hello", say_hello) # hello라는 이름으로 작업을 추가
graph.add_edge(START, "hello") # 시작 -> hello 작업으로 화살표를 그린다
graph.add_edge("hello", END) # hello -> 끝으로 화살표를 그린다

app = graph.compile() # 그래프를 실행 가능한 프로그램으로 만든다
result = app.invoke({"message": ""}) # invoke() 빈 메세지로 프로그램을 시작
print(result)