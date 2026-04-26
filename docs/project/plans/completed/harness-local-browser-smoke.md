# 하네스 템플릿 로컬 브라우저 smoke 재검증 결과

## 목적

full 하네스 템플릿을 별도 Git fixture에 적용한 뒤 `spec -> plan -> build` 흐름이 실제 로컬 브라우저 확인까지 이어지는지 재검증한다.

## 실행 대상

- fixture: `/tmp/harness-local-browser-smoke.7PijaP/project`
- fixture Git 브랜치: `main`
- fixture 최종 상태: clean
- 실제 브라우저 URL: `http://127.0.0.1:4173/`
- 브라우저 검증 도구: Playwright CLI fallback

## 배경

- `harness/templates/`와 `harness/source/full/root/`는 정적 검증을 통과한 상태에서 시작했다.
- 이전 smoke에서는 alias 라우팅과 파일 생성은 확인했지만, 로컬 서버 검증은 Codex sandbox의 TCP bind 제한으로 실패했다.
- 이번 재검증에서는 sandbox 밖 승인 실행으로 로컬 HTTP 서버와 Playwright CLI를 실행해 실제 브라우저 smoke를 완료했다.

## 범위

- `/tmp` 아래 새 Git fixture를 만든다.
- `harness/scripts/apply-template.py`로 full 템플릿을 적용한다.
- fixture에서 `spec`, `plan`, `build` alias를 `codex exec`로 실행한다.
- 생성된 앱을 로컬 서버로 열고 Playwright CLI로 DOM과 핵심 UI를 확인한다.
- root `SPEC.md`, `tasks/plan.md`, `tasks/todo.md`, `docs/references`가 생성되지 않는지 확인한다.
- 결과와 환경 제한 여부를 completed plan에 기록하고 커밋한다.

## 제외 항목

- 하네스 템플릿 구조 변경.
- `$harness-apply` 기능 변경.
- 모든 ExecPlan 항목 완료.
- 대상 fixture를 저장소에 추가.

## 진행 체크리스트

- [x] active plan을 작성한다.
- [x] 원 저장소의 템플릿 상태를 정적 검증한다.
- [x] 새 Git fixture를 만들고 full 템플릿을 적용한다.
- [x] `spec` smoke를 실행하고 product spec 생성을 확인한다.
- [x] `plan` smoke를 실행하고 active ExecPlan 생성을 확인한다.
- [x] `build` smoke를 실행하고 첫 구현 산출물을 확인한다.
- [x] 로컬 서버를 실행하고 Playwright로 브라우저 smoke를 수행한다.
- [x] forbidden legacy/reference 경로 부재와 fixture Git 상태를 확인한다.
- [x] 결과를 completed plan으로 이동하고 커밋한다.

## 검증 기록

| 날짜 | 항목 | 실행한 검증 | 결과 |
| --- | --- | --- | --- |
| 2026-04-26 | 템플릿 drift | `python3 harness/scripts/build-template.py --check` | 통과: `harness/source/full/root`와 `harness/templates`가 일치한다. |
| 2026-04-26 | 템플릿 정적 검증 | `python3 harness/scripts/validate-template.py` | 통과: `template validation ok`. |
| 2026-04-26 | 적용 dry-run | `python3 harness/scripts/apply-template.py --target /tmp/harness-local-browser-smoke.7PijaP/project --dry-run` | 통과: 56개 파일 복사 예정, 충돌 0. |
| 2026-04-26 | 적용 | `python3 harness/scripts/apply-template.py --target /tmp/harness-local-browser-smoke.7PijaP/project` | 통과: full 템플릿 적용 완료. |
| 2026-04-26 | fixture 초기 커밋 | `git init -b main`, `git add .`, `git commit -m "Apply full harness template"` | 통과: 초기 커밋 `7d4ca4e`. |
| 2026-04-26 | `spec` smoke | `codex exec --sandbox workspace-write "spec: ..."` | 통과: `docs/product-specs/browser-smoke-notes-app.md` 생성, 색인 갱신, fixture 커밋 `8e09b13`. |
| 2026-04-26 | `plan` smoke | `codex exec --sandbox workspace-write "plan: ..."` | 통과: `docs/exec-plans/active/browser-smoke-notes-app.md` 생성, fixture 커밋 `a70035f`. |
| 2026-04-26 | `build` smoke | `codex exec --sandbox workspace-write "build"` | 부분 통과: `index.html`, `styles.css`, `app.js` 구현과 ExecPlan 검증 기록 갱신. 일반 sandbox에서는 포트 bind와 Playwright 준비가 막혀 작업 1은 내부적으로 미완료로 남겼다. |
| 2026-04-26 | sandbox 밖 로컬 서버 | `python3 -m http.server 4173 --bind 127.0.0.1` | 통과: 승인 실행으로 `http://127.0.0.1:4173/` 서빙. |
| 2026-04-26 | 실제 브라우저 초기 smoke | `npx --yes --package @playwright/cli playwright-cli open http://127.0.0.1:4173 --headed`, `snapshot` | 통과: 앱 제목, 제목/내용 입력, 비활성 추가 버튼, 빈 상태, `총 0개` 표시 확인. |
| 2026-04-26 | 실제 브라우저 추가 smoke | Playwright CLI `fill`, `click`, `snapshot` | 통과: 메모 추가 후 목록 표시, 빈 상태 제거, `총 1개` 갱신 확인. |
| 2026-04-26 | 실제 브라우저 입력 안전성 | Playwright CLI로 `<script>alert(1)</script>` 입력 후 추가 | 통과: 문자열이 텍스트로 표시되고 총 `2개`로 갱신됐다. |
| 2026-04-26 | screenshot | Playwright CLI `screenshot` | 통과: fixture의 `.playwright-cli/page-2026-04-26T13-30-27-047Z.png` 생성. 해당 디렉터리는 fixture Git 추적에서 제외했다. |
| 2026-04-26 | fixture 정적 확인 | `node --check app.js`, `git diff --check` | 통과. |
| 2026-04-26 | forbidden path | `find`로 root `SPEC.md`, `tasks/plan.md`, `tasks/todo.md`, `docs/references` 확인 | 통과: 출력 없음. |
| 2026-04-26 | fixture 최종 상태 | `git status --short`, `git log --oneline --max-count=6` | 통과: status clean, 최종 커밋 `c6c7858`. |

## 발견 사항

- full 템플릿을 새 Git fixture에 적용한 뒤 `spec -> plan -> build` 흐름이 정상 라우팅됐다.
- `build`는 active ExecPlan의 첫 미완료 항목을 선택해 정적 앱 구현 파일을 생성하고 같은 ExecPlan에 검증 결과를 남겼다.
- 일반 sandbox에서는 로컬 포트 bind와 Playwright CLI 준비가 모두 제한됐다. 이 경우 `$harness-exec-build`가 체크박스를 완료 처리하지 않고 제한을 기록한 것은 기대한 안전 동작이다.
- sandbox 밖 승인 실행에서는 실제 로컬 서버와 Playwright 브라우저 smoke가 통과했다.
- Playwright 콘솔에는 앱 런타임 오류가 아니라 `favicon.ico` 404가 1건 관찰됐다. 기능 smoke 실패는 아니지만, 콘솔 청결을 기준에 포함한다면 대상 앱에 favicon 명시를 추가할 수 있다.
- 새 target 프로젝트에서 root `SPEC.md`, `tasks/plan.md`, `tasks/todo.md`, `docs/references`는 생성되지 않았다.

## 결정 로그

- 2026-04-26: 브라우저 플러그인의 Node REPL 도구가 현재 세션에 노출되지 않아, 실제 브라우저 확인은 Playwright CLI fallback으로 수행한다.
- 2026-04-26: 로컬 서버와 Playwright CLI 실행은 sandbox 제한을 우회하기 위해 사용자 승인 기반 escalated command로 수행한다.

## 완료 조건

- [x] 새 Git fixture에서 full 하네스 적용이 성공한다.
- [x] `spec`, `plan`, `build` alias가 새 하네스 계약대로 동작한다.
- [x] 로컬 브라우저에서 생성 앱의 핵심 화면을 확인한다.
- [x] 생성 금지 경로가 생기지 않는다.
- [x] 결과가 문서화되고 커밋되어 있다.

## 완료 후 처리

- completed plan으로 이동했다.
- fixture 경로와 커밋 로그를 문서에 남겼다.

## fixture 커밋 로그

| 커밋 | 내용 |
| --- | --- |
| `c6c7858` | 작업 1 정적 앱 구현, 실제 브라우저 smoke 결과 기록 |
| `a70035f` | 브라우저 smoke 메모 앱 active ExecPlan 생성 |
| `8e09b13` | 브라우저 smoke 메모 앱 product spec 생성 |
| `7d4ca4e` | full 하네스 템플릿 초기 적용 |

## 결론

full 하네스 템플릿은 다른 프로젝트에 복제해 repo-local `spec`, `plan`, `build` 흐름을 시작하는 용도에 적합하다. 실제 브라우저 smoke까지 확인하려면 현재 Codex sandbox 밖에서 로컬 서버와 브라우저 도구 실행 권한이 필요하지만, 권한이 주어진 환경에서는 `build` 산출물을 로컬 브라우저에서 검증할 수 있었다.
