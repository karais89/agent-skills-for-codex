# 오케스트레이션 패턴

이 문서는 여러 agent persona와 skill을 어떻게 조합할지 정하는 기준입니다. 핵심 원칙은 단순합니다.

**오케스트레이터는 사용자 또는 명시적인 command입니다. Persona가 다른 persona를 호출하지 않습니다.**

Skill은 persona 내부 workflow에서 사용할 수 있지만, persona 간 위임 구조를 만들면 비용과 복잡도가 빠르게 커집니다.

## 권장 패턴

### 1. 직접 호출

가장 기본적인 방식입니다. 하나의 persona가 하나의 관점으로 하나의 산출물을 만듭니다.

```text
user -> code-reviewer -> report -> user
```

사용할 때:

- 작업이 한 문장으로 설명됩니다.
- 하나의 관점이면 충분합니다.
- 비용과 latency를 최소화하고 싶습니다.

예시:

- "이 PR 리뷰해줘" -> `code-reviewer`
- "`auth.ts`의 보안 문제 찾아줘" -> `security-auditor`
- "checkout flow에 빠진 테스트 알려줘" -> `test-engineer`

### 2. 단일 persona wrapper

반복되는 단일 persona workflow를 command 또는 wrapper skill로 저장합니다.

```text
review or review: -> code-reviewer + code-review-and-quality skill -> report
```

사용할 때:

- 같은 준비 절차를 매번 반복합니다.
- persona는 하나만 필요합니다.
- 사용자에게 짧은 entrypoint를 제공하고 싶습니다.

이 저장소의 예:

- `review` or `review:`
- `test` or `test:`
- `code-simplify` or `code-simplify:`

주의: wrapper 내용이 대부분 "어떤 persona를 부를지 판단"이라면 불필요한 router입니다. 사용자가 persona를 직접 고르게 하는 편이 낫습니다.

### 3. 병렬 fan-out 후 merge

여러 persona가 같은 입력을 독립적으로 검토하고, main context에서 결과를 합칩니다.

```text
                     -> code-reviewer    -
ship or ship: -> fan out  --> security-auditor --> merge -> go/no-go + rollback
                     -> test-engineer    -
```

사용할 때:

- sub-task가 서로 독립적입니다.
- 각 persona가 다른 종류의 finding을 냅니다.
- merge 작업이 main context에서 감당 가능합니다.
- wall-clock latency를 줄이는 것이 중요합니다.

이 저장소의 예:

- `ship` or `ship:`

적용 전 확인:

- 모든 sub-agent를 동시에 실행해도 순서 문제가 없는가?
- 각 persona가 중복이 아닌 다른 관점을 제공하는가?
- merge 단계가 작고 명확한가?
- 병렬화 비용을 정당화할 만큼 작업 규모가 큰가?

### 4. 사용자가 주도하는 순차 pipeline

의존성이 있는 lifecycle은 사용자가 command를 순서대로 실행합니다.

```text
spec -> plan -> build -> test -> review -> ship
```

사용할 때:

- 앞 단계의 결과가 다음 단계의 입력입니다.
- 단계 사이에 사람의 판단이 필요합니다.
- 잘못된 방향을 초기에 바로잡아야 합니다.

자동 lifecycle orchestrator를 만들지 않는 이유:

- 단계 간 요약 과정에서 nuance가 사라집니다.
- 사람의 checkpoint가 없어집니다.
- 토큰 비용이 불필요하게 증가합니다.

### 5. 조사 격리

큰 코드베이스나 많은 문서를 읽어야 할 때 main context를 오염시키지 않도록 별도 조사 agent를 사용합니다.

```text
main agent -> research sub-agent -> digest -> main agent
```

사용할 때:

- 읽어야 할 입력이 많습니다.
- 최종 판단에는 요약만 필요합니다.
- main agent가 downstream 작업을 위해 context를 아껴야 합니다.

예시:

- deprecated API call site 전체 조사
- ADR 30개의 caching 관련 결정 요약
- 특정 module boundary가 어디서 깨지는지 조사

## Codex 적용 기준

이 저장소에서는 Codex 로컬 구조를 사용합니다.

- 스킬은 `.agents/skills`에 둡니다.
- agent role은 `.codex/agents`에 둡니다.
- hook은 `.codex/hooks.json`과 `.codex/hooks/*.py`에 둡니다.
- 전역 `~/.codex`, `~/.agents`, `/etc/codex`는 수정하지 않습니다.

Codex agent role은 모델을 명시하지 않으면 부모 세션 모델을 상속합니다. 이 저장소의 `code-reviewer`, `security-auditor`, `test-engineer`는 read-only review 성격이므로 `sandbox_mode = "read-only"`를 기본으로 합니다.

## Subagent와 팀 방식의 차이

| 항목 | 독립 subagent | 팀 방식 |
| --- | --- | --- |
| 조정 | main agent가 fan-out 후 결과를 합침 | agent끼리 대화하며 조사 |
| context | subagent마다 독립 context | teammate마다 독립 context |
| 적합한 경우 | 독립 보고서가 필요한 경우 | 가설을 서로 반박하며 좁혀야 하는 경우 |
| 비용 | 비교적 낮음 | 더 높음 |

`ship`/`ship:`은 독립 보고서를 합치는 verdict 작업입니다. 서로의 가설을 반박해야 하는 복잡한 root-cause debugging은 팀 방식이 더 적합할 수 있습니다.

## 예시: 경쟁 가설 디버깅

상황:

> checkout이 약 50회 중 1회 정도 30초 동안 멈춘 뒤 완료됩니다. 로그에는 오류가 없고 지난주 release 이후 시작됐습니다.

가능한 원인:

1. payment confirmation flow의 race condition
2. auth check가 느린 synchronous network call로 빠지는 경우
3. cart size에 따라 느려지는 query index 누락
4. SDK가 조용히 retry하는 flaky third-party API

단일 agent는 처음 그럴듯한 가설에 고정될 위험이 있습니다. `ship`/`ship:` fan-out은 독립 보고서를 만들지만, 보고서끼리 서로 반박하지는 않습니다. 이런 경우에는 여러 investigator가 서로의 가설을 깨는 방식이 더 낫습니다.

## 안티패턴

### A. Router persona

persona가 "어떤 persona를 부를지 결정"하는 역할만 한다면 불필요합니다. 사용자 또는 wrapper command가 라우팅해야 합니다.

문제:

- 토큰 비용 증가
- 책임 경계 불명확
- 실제 작업 전 불필요한 요약 발생

### B. Persona가 다른 persona를 호출

`code-reviewer`가 `security-auditor`를 호출하는 식의 구조를 만들지 않습니다. 필요하면 report에서 "보안 전담 리뷰가 필요하다"고 권고하고, 사용자가 실행하게 합니다.

### C. 순차 orchestrator가 결과를 재서술

각 단계 결과를 다음 단계에 넘기며 계속 요약하는 orchestrator는 정보 손실과 비용 증가를 만듭니다. 순차 workflow는 사용자가 직접 단계별로 실행하는 편이 안전합니다.

### D. 깊은 persona tree

agent가 agent를 부르고 다시 agent를 부르는 구조는 추적과 검증이 어렵습니다. 이 저장소에서는 최대한 얕은 구조를 유지합니다.

## 결정 흐름

```text
작업이 하나의 관점으로 충분한가?
  yes -> 직접 호출
  no  -> 다음 질문

여러 관점이 서로 독립적인가?
  yes -> 병렬 fan-out 후 merge
  no  -> 다음 질문

단계 사이에 명확한 의존성과 사람의 판단이 필요한가?
  yes -> 사용자가 주도하는 순차 pipeline
  no  -> 조사 격리 또는 작업 재정의
```

## 새 패턴을 추가할 때

새 오케스트레이션 패턴은 다음 조건을 만족할 때만 추가합니다.

- 기존 패턴으로 설명되지 않습니다.
- 비용과 복잡도 증가를 정당화합니다.
- 실패 mode와 검증 방법이 명확합니다.
- persona 간 책임 경계가 흐려지지 않습니다.
