---
name: harness-apply
description: full 하네스 템플릿을 다른 프로젝트 루트에 적용한다. 대상 디렉터리에 repo-local .agents, .codex, AGENTS.md, README.md, docs/product-specs, docs/exec-plans 구조를 복제해야 할 때, 또는 적용 전 dry-run/충돌 검사가 필요할 때 사용한다.
---

# Harness Apply

full 배포 모델의 하네스 템플릿을 대상 프로젝트 루트에 적용한다. 이 스킬은 템플릿 내용을 수정하지 않고, `harness/scripts/apply-template.py`를 사용해 충돌 없는 복제만 수행한다.

## Workflow

1. 대상 프로젝트 루트를 확인한다.
   - 사용자가 경로를 주지 않았으면 적용 대상을 먼저 물어본다.
   - 새 프로젝트이면 존재하지 않는 디렉터리 경로를 사용할 수 있다.
   - 기존 프로젝트이면 Git 상태와 충돌 가능성을 먼저 확인한다.
2. 이 저장소의 템플릿 상태를 확인한다.
   - `python3 harness/scripts/build-template.py --check`
   - `python3 harness/scripts/validate-template.py`
3. 적용 전 dry-run을 실행한다.
   - `python3 harness/scripts/apply-template.py --target <target> --dry-run`
   - 충돌이 있으면 적용하지 말고 충돌 경로를 사용자에게 보고한다.
4. dry-run이 통과하면 실제 적용을 실행한다.
   - `python3 harness/scripts/apply-template.py --target <target>`
5. 적용 결과를 확인한다.
   - 대상에 `AGENTS.md`, `.codex/hooks.json`, `.agents/skills/`, `docs/product-specs/`, `docs/exec-plans/`가 있는지 확인한다.
   - 대상에 root `SPEC.md`, `tasks/plan.md`, `tasks/todo.md`, `docs/references`가 새로 생기지 않았는지 확인한다.
   - 대상이 Git 저장소이면 `git status --short`로 적용 변경을 확인한다.
6. 사용자가 smoke 검증을 요청했거나 적용 품질을 확인해야 하면 대상 프로젝트에서 `codex exec` 시뮬레이션을 실행한다.
   - 예: `codex exec --sandbox workspace-write "spec: ..."`
   - 예: `codex exec --sandbox workspace-write "plan: ..."`
   - 예: `codex exec --sandbox workspace-write "build"`

## Rules

- 지원 배포 모델은 `full` 하나다.
- 기본 적용 소스는 `harness/templates/`다.
- `harness/source/full/root/`를 직접 수정하거나 `harness/templates/`를 직접 편집하지 않는다.
- 충돌이 있는 기존 파일은 덮어쓰지 않는다.
- 자동 병합, 백업, 강제 덮어쓰기는 이 스킬의 범위가 아니다.
- 대상 프로젝트에 root `SPEC.md`, `tasks/plan.md`, `tasks/todo.md`, `docs/references`를 만들지 않는다.
- `$harness-apply` 자체는 대상 프로젝트 템플릿에 번들하지 않는다.

## Commands

```bash
python3 harness/scripts/apply-template.py --target /path/to/project --dry-run
python3 harness/scripts/apply-template.py --target /path/to/project
```

검증 명령:

```bash
python3 harness/scripts/test-apply-template.py
python3 harness/scripts/build-template.py --check
python3 harness/scripts/validate-template.py
```
