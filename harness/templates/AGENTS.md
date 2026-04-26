# Codex 하네스 지침

이 프로젝트는 repo-local Codex 하네스를 사용한다. 이 프로젝트를 위해 `~/.codex`, `~/.agents`, `/etc/codex` 같은 전역 설정을 수정하지 않는다.

## 로컬 구조

- `.agents/skills/`: 이 프로젝트에서 사용하는 로컬 스킬과 wrapper 스킬을 둔다.
- `.codex/agents/`: 코드 리뷰, 보안 점검, 테스트 점검용 로컬 Codex 역할을 둔다.
- `.codex/hooks.json`, `.codex/hooks/*.py`: alias routing과 안전 정책을 정의한다.
- `docs/product-specs/`: 제품 요구사항과 수용 기준을 둔다.
- `docs/exec-plans/`: 장시간 작업과 큰 변경의 실행 계획을 둔다.
- `docs/references/`: 테스트, 보안, 성능, 접근성, 오케스트레이션 참고 문서를 둔다.

## Alias 매핑

Codex TUI는 알 수 없는 `/spec` 같은 입력을 prompt가 아니라 slash command로 먼저 해석한다. 프로젝트 정의 slash command는 사용하지 않는다. 직접 호출할 때는 `$harness-product-spec`처럼 실제 스킬 이름을 사용한다.

| Alias | Codex 스킬 | 산출물 |
| --- | --- | --- |
| `spec`, `spec:` | `$harness-product-spec` | `docs/product-specs/<slug>.md` |
| `plan`, `plan:` | `$harness-exec-plan` | `docs/exec-plans/active/<slug>.md` |
| `build`, `build:` | `$harness-exec-build` | active ExecPlan의 다음 미완료 항목 |
| `test`, `test:` | `$agent-skills-test` | TDD와 검증 workflow |
| `review`, `review:` | `$agent-skills-review` | 5축 코드 리뷰 |
| `code-simplify`, `code-simplify:` | `$agent-skills-code-simplify` | 동작 보존 단순화 |
| `ship`, `ship:` | `$agent-skills-ship` | 출시 go/no-go 검토 |

`spec`, `plan`, `build` workflow에서는 루트 `SPEC.md`, `tasks/plan.md`, `tasks/todo.md`를 만들지 않는다.

## 작업 기준

- 작업 전 관련 문서와 현재 Git 상태를 확인한다.
- 변경 범위는 사용자 요청과 active ExecPlan에 맞게 제한한다.
- 큰 변경은 `docs/exec-plans/active/`의 실행 계획을 먼저 만들거나 갱신한다.
- 구현 후에는 관련 검증을 실행하고 결과를 ExecPlan 또는 완료 보고에 남긴다.
- 사용자가 만들었을 수 있는 변경은 되돌리지 않는다.

## 전문 에이전트

- `code-reviewer`: correctness, readability, architecture, security, performance 다섯 축으로 코드 리뷰를 수행한다.
- `security-auditor`: 실제 악용 가능성이 있는 취약점과 위협 모델을 점검한다.
- `test-engineer`: 테스트 전략, coverage gap, Prove-It 버그 재현 테스트를 다룬다.

전문 에이전트는 기본적으로 read-only 검토 역할이다. subagent로 호출할 때는 `spawn_agent`의 `agent_type`에 위 역할 이름을 사용한다.

## Hook 정책

- `SessionStart`: 로컬 스킬 라우팅 컨텍스트를 주입한다.
- `UserPromptSubmit`: 텍스트 alias를 wrapper 스킬로 안내한다.
- `PreToolUse`: 넓은 범위의 파괴적 shell 명령과 보호 블록 수정을 차단한다.
- `PostToolUse`: 실패한 tool 결과 뒤에 debugging/verification 컨텍스트를 제공한다.
- `Stop`: 변경 완료 응답에 검증 내용이 빠진 경우 continuation reason을 반환한다.
