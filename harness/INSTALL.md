# Harness 설치 지침

이 문서는 LLM 코딩 에이전트가 읽고 수행하기 위한 설치 지침이다. 사용자는 복잡한 명령을 직접 실행하지 않고, 에이전트에게 이 문서를 읽고 새 프로젝트를 준비하라고 요청한다.

## Source

- public repository: `https://github.com/karais89/agent-skills-for-codex`
- raw install guide: `https://raw.githubusercontent.com/karais89/agent-skills-for-codex/main/harness/INSTALL.md`
- default template source: `harness/templates/`
- apply script: `harness/scripts/apply-template.py`

## 지원하는 작업

1. 새 프로젝트 생성
2. 기존 프로젝트에 하네스 적용

우선순위는 새 프로젝트 생성이다. 기존 프로젝트 적용은 충돌이 없는 경우에만 수행한다.

## 공통 원칙

- `harness/templates/`를 사람이 직접 복사하게 하지 않는다.
- 이 저장소를 로컬에 클론한 뒤 `harness/scripts/apply-template.py`를 사용한다.
- 적용 전 항상 dry-run을 실행한다.
- 충돌이 있으면 적용하지 말고 충돌 경로를 보고한다.
- 대상 프로젝트에 root `SPEC.md`, `tasks/plan.md`, `tasks/todo.md`, `docs/references`를 만들지 않는다.
- `README.md`, `ARCHITECTURE.md`, `AGENTS.md`, `docs/validation.md`는 대상 프로젝트에 맞게 초기화한다.
- 사용자가 이미 작성한 파일은 덮어쓰지 않는다.

## 새 프로젝트 생성 절차

필수 입력:

- 대상 경로
- 프로젝트 이름
- 프로젝트 목적 또는 한 줄 설명

절차:

1. 하네스 소스 저장소를 사용할 수 있는지 확인한다.
   - 이미 로컬 경로가 주어졌으면 그 경로를 사용한다.
   - 없으면 임시 디렉터리에 `https://github.com/karais89/agent-skills-for-codex.git`를 클론한다.
2. 대상 경로를 확인한다.
   - 존재하지 않으면 생성한다.
   - 존재하지만 비어 있지 않으면 새 프로젝트 생성으로 진행하지 말고 사용자에게 기존 프로젝트 적용 절차로 전환할지 확인한다.
3. 소스 저장소에서 템플릿 상태를 확인한다.
   - `python3 harness/scripts/build-template.py --check`
   - `python3 harness/scripts/validate-template.py`
4. dry-run을 실행한다.
   - `python3 harness/scripts/apply-template.py --target <target> --dry-run`
5. 충돌이 없으면 실제 적용을 실행한다.
   - `python3 harness/scripts/apply-template.py --target <target>`
6. 대상 프로젝트 문서를 초기화한다.
   - `README.md`: 프로젝트 이름, 목적, 초기 상태, 하네스 사용 흐름을 반영한다.
   - `ARCHITECTURE.md`: 아직 구현이 없다면 그렇게 명시하고, 앞으로 기록할 구조 항목을 프로젝트 목적 기준으로 정리한다.
   - `AGENTS.md`: 하네스 공통 지침은 유지하되, 프로젝트 이름과 현재 검증 명령 상태를 짧게 추가한다.
   - `docs/validation.md`: 현재 실행 가능한 검증은 하네스 설정 검증뿐임을 기록한다. 앱 코드가 아직 없다면 테스트 명령은 "아직 없음"으로 적는다.
7. 대상 프로젝트를 Git 저장소로 초기화한다.
   - 이미 Git 저장소가 아니면 `git init`을 실행한다.
   - 생성된 파일을 커밋할 수 있으면 `Initial harness project setup` 메시지로 커밋한다.
8. 검증한다.
   - `.codex/hooks.json` JSON 파싱
   - `.codex/config.toml`, `.codex/agents/*.toml` TOML 파싱
   - `.agents/skills/*/SKILL.md` frontmatter 존재 확인
   - `python3 .codex/hooks/user_prompt_submit.py`로 `spec`, `plan`, `build` alias routing 확인
   - forbidden path 미생성 확인
   - Git 상태 확인
9. 결과를 보고한다.
   - 대상 경로
   - 생성/수정 파일 요약
   - 실행한 검증과 결과
   - 커밋 hash
   - 남은 수동 작업

## 기존 프로젝트 적용 절차

필수 입력:

- 대상 프로젝트 경로
- 프로젝트 이름 또는 현재 프로젝트 목적

절차:

1. 대상 경로가 Git 저장소인지 확인하고 현재 상태를 기록한다.
2. 하네스 소스 저장소의 템플릿 상태를 확인한다.
3. dry-run을 실행한다.
4. 충돌이 있으면 실제 적용하지 않는다.
5. 충돌이 없으면 실제 적용한다.
6. 대상 프로젝트의 기존 코드와 문서를 읽고 `README.md`, `ARCHITECTURE.md`, `AGENTS.md`, `docs/validation.md`를 실제 프로젝트 기준으로 초기화하거나 보강한다.
7. 기존 테스트 명령이 있으면 실행한다.
8. forbidden path 미생성, alias routing, config parsing을 확인한다.
9. 변경 사항을 커밋할 수 있으면 커밋한다.

## 문서 초기화 기준

`README.md`에는 최소한 다음 내용이 있어야 한다.

- 프로젝트 이름
- 프로젝트 목적
- 현재 구현 상태
- 빠른 시작 또는 아직 정해지지 않았다는 명시
- 검증 명령
- `spec -> plan -> build` 사용 흐름

`ARCHITECTURE.md`에는 최소한 다음 내용이 있어야 한다.

- 시스템 목적
- 현재 구현 상태
- 주요 구성요소 또는 아직 없다는 명시
- 데이터와 상태의 현재 기준
- 인터페이스의 현재 기준
- 알려진 제약

`AGENTS.md`에는 최소한 다음 내용이 있어야 한다.

- 하네스 공통 지침
- 이 프로젝트의 이름과 목적
- 현재 사용 가능한 검증 명령
- 큰 변경은 `docs/exec-plans/active/`를 기준으로 진행한다는 지침

`docs/validation.md`에는 최소한 다음 내용이 있어야 한다.

- 하네스 설정 검증 명령
- 앱 테스트 명령이 있으면 그 명령
- 앱 테스트 명령이 없으면 아직 없다고 명시

## 완료 보고 형식

완료 보고는 짧게 작성한다.

```text
하네스 설정 완료:
- 대상: <target>
- 프로젝트: <name>
- 적용: 성공/실패
- 검증: <commands and results>
- 커밋: <hash or none>
- 다음 단계: codex에서 spec:, plan:, build 사용
```
