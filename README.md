## ex01에서 만든 그래프 모양

<img width="106" height="234" alt="1-1-1" src="https://github.com/user-attachments/assets/0239b63e-1d96-4cc4-8e6c-46556ffd74ad" />


### START: 프로그램 시작점

### hello: say_hello 함수가 실행되는 노드

### END: 프로그램 종료점

---

## ex03에서 만든 노드 연결 그래프

<img width="106" height="333" alt="1-3-1b" src="https://github.com/user-attachments/assets/d7bf8362-ce35-44fb-9124-5505b5259e46" />

---

# echo_chat_v2
# LangGraph Practice (Messages + Tools + Gemini)

LangGraph로 **상태 기반 대화(messages)** 를 구성하고, LLM이 필요하면 **Tool(calc)** 를 호출한 뒤 결과를 바탕으로 답변하는 기본 에이전트 루프를 연습하는 프로젝트입니다.

- 상태(State): `messages` 리스트 (누적)
- 체크포인터: `InMemorySaver` + `thread_id`로 멀티턴 유지
- 툴 호출: `ToolNode` + `tools_condition`
- LLM: `openai_client.gemini` 래퍼 사용 (`bind_tools`, `invoke` 지원 가정)

---

## Features

- messages 기반 멀티턴 대화 상태 관리 (`add_messages`)
- LLM이 tool call을 만들면 자동으로 ToolNode 실행
- 계산 툴 `calc(expression)` 제공 (`2+3`, `10-7`, `4*5`, `8/2`)
- tool 결과를 반영해 최종 답변 생성 (LLM이 생성)

---

## Requirements

- Python: **3.11 ~ 3.12 권장**
  - Python 3.14에서는 `pydantic v1` 관련 경고/호환 이슈가 발생할 수 있습니다.
- 패키지:
  - `langgraph`
  - `langchain-core`
  - (툴/모델 연동에 따라) `langchain` 또는 해당 provider 패키지

> `openai_client.gemini`는 프로젝트 내/개인 래퍼로 가정합니다.  
> 이 객체는 **`.bind_tools(tools)`**, **`.invoke(messages)`** 를 지원해야 합니다.

