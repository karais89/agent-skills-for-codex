# 다운로드한 참고 저장소 분석

확인일: 2026-04-26

대상 경로: `reference-repos/adopted/`, `reference-repos/supporting/`

## 분석 기준

이 문서는 다운로드한 참고 저장소를 그대로 벤더링하거나 복제하기 위한 문서가 아니다. 이 프로젝트에서 재사용할 수 있는 에이전트 운영 원칙, 스킬 구성 방식, 문서 구조, 검증 루프, 하네스 설계 패턴을 추려서 비교한다.

## 전체 결론

현재 참고 저장소들은 크게 세 계열로 나뉜다.

| 계열 | 저장소 | 핵심 가치 |
| --- | --- | --- |
| 실제 제품 구현체 | `openai-codex` | 대규모 에이전트 CLI의 모듈화, 엄격한 지침, 테스트와 리뷰 체계 |
| 스킬·방법론 라이브러리 | `andrej-karpathy-skills`, `superpowers`, `gstack`, `agent-skills` | 에이전트 행동을 재현 가능한 워크플로우로 고정 |
| 하네스 템플릿 | `harness_framework` | 장시간 작업을 phase/step 단위로 나누고 자동 실행·커밋·재시도 |

이 프로젝트에는 `agent-skills`의 균형 잡힌 생명주기 구조, `superpowers`의 강한 계획·검증 규율, `gstack`의 전문 역할 분리, `karpathy-guidelines`의 보수적 행동 원칙, `harness_framework`의 phase/step 실행 구조를 선별적으로 섞는 것이 적합하다. `openai-codex`는 직접 구조를 따라 하기보다 “실제 대규모 에이전트 제품은 지침과 테스트를 얼마나 구체적으로 갖추는가”를 보는 기준점으로 쓰는 편이 낫다.

## 저장소별 분석

### openai-codex

로컬 경로: `reference-repos/supporting/openai-codex`

성격: OpenAI Codex CLI의 실제 구현 저장소다. Rust 워크스페이스가 중심이며, CLI, TUI, 프로토콜, 샌드박스, MCP, 플러그인, 스킬, 앱 서버 등 많은 크레이트로 세분화되어 있다.

주요 관찰:

- `AGENTS.md`가 매우 구체적이다. Rust 스타일, 테스트 명령, API 네이밍, Bazel/Cargo 차이, 스냅샷 테스트, 큰 모듈 회피 같은 실무 규칙을 직접 명시한다.
- `.codex/skills/`에는 코드 리뷰, 테스트, PR 본문 작성, PR 감시 같은 운영 스킬이 들어 있다.
- 코드 리뷰 스킬은 오케스트레이터와 세부 검토 스킬을 분리한다. 예를 들어 `code-review`가 여러 `code-review-*` 스킬을 병렬 리뷰 단위로 다룬다.
- 변경 크기 제한, 테스트 작성 기준, PR 본문에서 “왜”를 먼저 설명하는 규칙처럼 리뷰 품질을 높이는 작은 규칙이 많다.
- Apache-2.0 라이선스가 명시되어 있다.

이 프로젝트에 참고할 점:

- `AGENTS.md`는 짧게 유지하되, 기술 스택이 정해지면 언어별·도구별 세부 규칙은 별도 문서로 분리한다.
- 코드 리뷰는 단일 “좋아 보임” 평가가 아니라 변경 크기, 테스트, 호환성, 맥락 같은 축으로 나눈다.
- 사용자에게 보이는 UI나 출력이 바뀌면 스냅샷 또는 화면 검증을 요구하는 규칙을 둘 수 있다.
- 큰 공통 모듈에 기능을 계속 추가하지 말고, 새 개념은 적절한 모듈로 분리하는 원칙을 둔다.

주의할 점:

- 저장소 규모가 매우 크고 제품 구현 세부가 많아, 이 프로젝트 초기에 구조를 직접 모방하면 과설계가 될 가능성이 높다.
- Rust/Bazel 특화 규칙은 현재 프로젝트에 그대로 적용하지 않는다.

### andrej-karpathy-skills

로컬 경로: `reference-repos/adopted/andrej-karpathy-skills`

성격: 단일 행동 지침에 가까운 경량 스킬 저장소다. 핵심은 “생각한 뒤 코딩, 단순성 우선, 외과적 변경, 목표 기반 실행” 네 가지 원칙이다.

주요 관찰:

- 구조가 매우 작다. `CLAUDE.md`와 `skills/karpathy-guidelines/SKILL.md`가 사실상 핵심이다.
- LLM 코딩에서 흔한 실패, 즉 잘못된 가정, 과한 추상화, 주변 코드 변경, 검증 없는 완료 선언을 직접 겨냥한다.
- 스킬 설명이 명확해서 거의 모든 코딩·리뷰·리팩터링 상황에 적용할 수 있다.
- README는 MIT 라이선스라고 설명하지만, 로컬 클론에는 별도 `LICENSE` 파일이 보이지 않았다.

이 프로젝트에 참고할 점:

- 모든 작업에 적용되는 기본 행동 원칙으로 가장 적합하다.
- “모든 변경 라인은 사용자 요청과 직접 연결되어야 한다”는 기준은 이 프로젝트의 기본 품질 규칙으로 삼을 만하다.
- 성공 기준을 먼저 정의하고 검증 루프를 돌리는 원칙은 실행 계획 문서와 잘 맞는다.

주의할 점:

- 단일 지침만으로는 스킬 설치, 브라우저 검증, 릴리스, 보안 검토 같은 운영 체계가 부족하다.
- 지침이 보수적이므로 단순한 작업까지 과도하게 느려지지 않도록 적용 강도를 조절해야 한다.

### superpowers

로컬 경로: `reference-repos/supporting/superpowers`

성격: 코딩 에이전트용 종합 개발 방법론이다. 브레인스토밍, 계획, TDD, 실행, 코드 리뷰, 검증, 브랜치 마무리까지 하나의 워크플로우로 묶는다.

주요 관찰:

- `skills/` 아래에 14개 스킬이 있다.
- 기본 흐름은 `brainstorming` → `using-git-worktrees` → `writing-plans` → `subagent-driven-development` 또는 `executing-plans` → `test-driven-development` → `requesting-code-review` → `finishing-a-development-branch`이다.
- 계획 문서 작성 규칙이 강하다. 각 단계는 2~5분 단위, 정확한 파일 경로, 테스트 코드, 실행 명령, 기대 결과, 커밋 명령까지 포함해야 한다.
- `subagent-driven-development`는 작업자, 스펙 준수 리뷰어, 코드 품질 리뷰어를 분리한다.
- 기여 지침은 스킬 문구를 “행동을 바꾸는 코드”로 취급하며, 스킬 수정에는 평가 근거를 요구한다.
- MIT 라이선스가 있다.

이 프로젝트에 참고할 점:

- 장시간 작업은 계획 문서를 만들고, 체크박스로 상태를 남기며, 작은 단위로 커밋하는 방식을 채택한다.
- TDD와 검증 전 완료 금지를 강하게 둔다.
- 코드 리뷰를 스펙 준수와 코드 품질로 분리하는 패턴은 실제 품질 향상에 유용하다.
- 스킬 자체를 수정할 때는 “좋은 문장”이 아니라 “행동이 개선되는가”를 기준으로 평가해야 한다.

주의할 점:

- 규율이 매우 강해서 작은 프로젝트나 빠른 탐색 단계에는 부담이 클 수 있다.
- 계획 문서에 완전한 코드까지 요구하는 방식은 일부 상황에서 문서가 과하게 커질 수 있다.

### gstack

로컬 경로: `reference-repos/supporting/gstack`

성격: Claude Code 중심의 고밀도 AI 엔지니어링 워크플로우다. CEO, 엔지니어링 매니저, 디자이너, QA, 보안, 릴리스 엔지니어 같은 역할을 slash command와 스킬로 나눈다.

주요 관찰:

- 루트 주변에 40개 이상 `SKILL.md`가 있다.
- `/office-hours`, `/plan-ceo-review`, `/plan-eng-review`, `/plan-design-review`, `/review`, `/qa`, `/ship`, `/browse`, `/cso`, `/autoplan` 등 역할 기반 명령이 매우 많다.
- 프론트엔드 디자인, 브라우저 검증, 보안 감사, 릴리스, 배포 후 카나리, 성능 벤치마크까지 운영 범위가 넓다.
- `AGENTS.md`는 “스킬은 생성물이며 템플릿을 수정하라” 같은 저장소 내부 운영 규칙을 명시한다.
- `autoplan` 같은 스킬은 여러 리뷰 단계를 자동화하고, 사용자에게는 취향이나 범위 결정처럼 사람이 판단해야 하는 부분만 노출한다.
- Bun, Playwright, Puppeteer, Claude Agent SDK 등 실행 도구 의존성이 있다.
- MIT 라이선스가 있다.

이 프로젝트에 참고할 점:

- 역할을 세분화하는 방식이 강력하다. 특히 제품 검토, 엔지니어링 검토, 디자인 검토, QA 검토를 분리하는 구조는 적용 가치가 높다.
- UI 작업에는 실제 브라우저 조작과 스크린샷 기반 검증을 기본으로 넣을 수 있다.
- `/document-release`처럼 기능 출시 후 문서를 갱신하는 전용 단계는 이 프로젝트의 “모든 문서는 한글” 지침과 잘 맞는다.
- `careful`, `freeze`, `guard` 같은 안전 스킬 개념은 파일 범위 제한이나 위험 명령 차단 규칙으로 참고할 수 있다.

주의할 점:

- 기능 범위가 매우 넓어 그대로 가져오면 초기 프로젝트가 무거워진다.
- 로컬 홈 디렉터리, 텔레메트리, 자동 업데이트, 브라우저 서버 등 개인 환경에 강하게 결합된 부분은 그대로 복사하지 않는다.
- 이 프로젝트에는 우선 핵심 역할과 평가 기준만 추려서 작게 시작하는 편이 좋다.

### agent-skills

로컬 경로: `reference-repos/adopted/agent-skills`

성격: 개발 생명주기를 기준으로 정리된 범용 에이전트 스킬 라이브러리다. define, plan, build, verify, review, ship 흐름이 명확하다.

주요 관찰:

- `skills/` 아래에 21개 스킬이 있다.
- `/spec`, `/plan`, `/build`, `/test`, `/review`, `/code-simplify`, `/ship` 같은 명령이 개발 단계와 직접 대응한다.
- `AGENTS.md`는 스킬, 페르소나, slash command를 명확히 구분한다.
- 스킬은 “how”, 페르소나는 “who”, slash command는 “when”으로 정의한다.
- `context-engineering` 스킬은 규칙 파일, 스펙·아키텍처 문서, 관련 소스, 에러 출력, 대화 기록을 계층적으로 다루는 방식을 설명한다.
- `git-workflow-and-versioning` 스킬은 원자적 커밋, 짧은 브랜치, 변경 크기 관리, 커밋을 저장점으로 쓰는 패턴을 정리한다.
- `agents/`에는 코드 리뷰어, 테스트 엔지니어, 보안 감사자 페르소나가 있다.
- MIT 라이선스가 있다.

이 프로젝트에 참고할 점:

- 이 프로젝트의 기본 문서 체계는 `agent-skills`식 생명주기 구조를 따르는 것이 가장 균형적이다.
- `AGENTS.md`에는 큰 지침만 두고, 세부 스킬과 페르소나는 별도 파일로 분리한다.
- 컨텍스트 계층 구조는 `docs/README.md`와 향후 프로젝트 맵 문서 설계에 바로 적용할 수 있다.
- 커밋 자동화 지침은 이미 추가했으므로, 나중에 커밋 메시지 규칙과 변경 크기 기준을 더 구체화할 수 있다.

주의할 점:

- 스킬이 많기 때문에 처음부터 전부 도입하면 사용자가 어떤 스킬을 언제 써야 하는지 흐려질 수 있다.
- 범용성이 높은 대신, gstack처럼 강한 제품·디자인 취향을 주입하는 부분은 상대적으로 약하다.

### harness_framework

로컬 경로: `reference-repos/supporting/harness_framework`

성격: 한국어 기반의 장시간 작업 실행 하네스 템플릿이다. 문서 템플릿, phase/step 구조, 실행 스크립트를 갖춘다.

주요 관찰:

- `CLAUDE.md`, `docs/PRD.md`, `docs/ARCHITECTURE.md`, `docs/ADR.md`, `docs/UI_GUIDE.md`가 템플릿 형태로 있다.
- `.claude/commands/harness.md`는 탐색, 논의, step 설계, 파일 생성, 실행까지의 전체 워크플로우를 정의한다.
- `scripts/execute.py`는 `phases/{task}/index.json`과 `stepN.md`를 읽어 순차 실행한다.
- 실행기는 브랜치 생성, 가드레일 주입, 이전 step summary 누적, 최대 3회 재시도, 상태 전이, 커밋 분리를 처리한다.
- 상태는 `pending`, `completed`, `error`, `blocked`로 관리하고, 타임스탬프와 summary를 누적한다.
- `.claude/settings.json`은 Stop hook에서 lint/build/test를 돌리고, 위험 명령을 차단하는 예시를 담는다.
- 별도 라이선스 파일은 보이지 않았다.

이 프로젝트에 참고할 점:

- 한국어 문서 중심이라는 점에서 현재 프로젝트와 궁합이 좋다.
- `phases/index.json`과 `phases/{task}/stepN.md` 구조는 실행 계획보다 더 기계적인 장시간 작업 관리 방식으로 참고할 만하다.
- 각 step이 독립 세션에서 실행될 수 있도록 필요한 파일과 금지사항을 모두 포함하는 원칙은 중요하다.
- 완료 summary를 다음 step의 컨텍스트로 넘기는 방식은 컨텍스트 관리에 유용하다.

주의할 점:

- 현재 구현은 Claude CLI에 강하게 결합되어 있다. Codex용으로 쓰려면 실행기 호출부와 권한 모델을 바꿔야 한다.
- `git add -A` 같은 넓은 스테이징은 현재 프로젝트 지침상 주의가 필요하다. 적용 시 변경 범위를 더 좁게 검증해야 한다.
- 템플릿 수준의 문서가 많아 실제 프로젝트 지식으로 채우지 않으면 형식만 남을 수 있다.

## 비교와 적용 우선순위

| 우선순위 | 도입할 패턴 | 참고 저장소 | 이유 |
| --- | --- | --- | --- |
| 1 | 짧은 `AGENTS.md` + 상세 `docs/` | OpenAI Harness, `agent-skills`, `harness_framework` | 컨텍스트를 작게 유지하면서 지식을 저장소에 남길 수 있다. |
| 2 | 보수적 행동 원칙 | `andrej-karpathy-skills` | 과설계, 가정, 불필요한 변경을 줄인다. |
| 3 | 실행 계획과 작은 커밋 | OpenAI Exec Plans, `superpowers`, `agent-skills` | 긴 작업을 중단·재개·리뷰하기 쉬워진다. |
| 4 | 역할 분리 리뷰 | `gstack`, `superpowers`, `agent-skills` | 스스로 만든 결과를 스스로 과대평가하는 문제를 줄인다. |
| 5 | 브라우저 기반 UI 검증 | `gstack`, Anthropic 하네스 문서 | 프론트엔드 품질과 실제 사용자 흐름 검증에 필요하다. |
| 6 | phase/step 실행 하네스 | `harness_framework` | 장시간 자동 실행을 가능하게 하지만, 초기에 바로 도입하기엔 구현 부담이 있다. |

## 권장 문서 구조

당장 이 프로젝트에 추가할 수 있는 구조는 다음 정도가 적절하다.

```text
docs/
├── README.md
├── project/
│   ├── README.md
│   ├── principles/
│   │   ├── coding-agent-behavior.md
│   │   ├── git-workflow.md
│   │   └── review-quality-gates.md
│   └── plans/
│       ├── active/
│       └── completed/
├── references/
│   ├── README.md
│   ├── adopted/
│   ├── supporting/
│   └── analyses/
```

```text
harness/
├── README.md
├── templates/
├── skills/
└── scripts/
```

아직 실제 제품 코드가 없으므로 `src/` 구조나 기술 스택 문서를 먼저 만들기보다, 에이전트 작업 방식과 문서 운영 규칙부터 정리하는 편이 낫다.

## 다음 단계 제안

1. `karpathy-guidelines`, `agent-skills`, `superpowers`에서 공통으로 반복되는 원칙을 합쳐 `docs/project/principles/coding-agent-behavior.md`를 만든다.
2. `agent-skills`의 생명주기를 기준으로 `spec → plan → build → verify → review → ship` 문서 흐름을 정의한다.
3. OpenAI Exec Plans와 `superpowers/writing-plans`를 비교해 `harness/templates/` 아래에 대상 프로젝트용 실행 계획 템플릿을 만든다.
4. `harness_framework`를 Codex 친화적으로 이식할지 검토한다. 이때 넓은 `git add -A`, Claude CLI 직접 호출, hook 명령을 그대로 쓰지 않는다.
5. UI 작업이 생기면 `gstack`과 Anthropic 문서의 평가 기준을 참고해 브라우저 검증 체크리스트를 만든다.

## 라이선스 메모

- `openai-codex`: Apache-2.0
- `agent-skills`: MIT
- `gstack`: MIT
- `superpowers`: MIT
- `andrej-karpathy-skills`: README에는 MIT로 표기되어 있으나 로컬 클론에서 별도 `LICENSE` 파일은 확인되지 않았다.
- `harness_framework`: 로컬 클론에서 별도 `LICENSE` 파일은 확인되지 않았다.

외부 저장소의 코드를 직접 복사할 때는 라이선스와 저작권 고지를 별도로 확인해야 한다. 현재 문서는 패턴 분석과 운영 참고용이다.
