---
name: agent-skills-ship
description: Runs the original ship command fan-out workflow as a Codex skill. Use when the user types ship or ship:, invokes $agent-skills-ship, or wants a launch readiness go/no-go review.
---

# Agent Skills Ship

Use this skill when the user types `ship`, `ship:`, invokes `$agent-skills-ship`, asks for launch readiness, or wants a production go/no-go decision. Bare `/ship` is not supported by Codex TUI; it is rejected before hooks run.

Workflow:
1. Invoke and follow the `shipping-and-launch` skill.
2. Treat this as a fan-out orchestrator for production-bound changes. Run three specialist reports independently, then merge them in the main context.
3. Skip fan-out only when all are true: the change touches 2 files or fewer, the diff is under 50 lines, and it does not touch auth, payments, data access, or config/env.

Phase A: specialist reports
1. For non-trivial changes, run three Codex subagents concurrently when subagents are available. Call `spawn_agent` three times before any `wait_agent`, with `agent_type = "code-reviewer"`, `agent_type = "security-auditor"`, and `agent_type = "test-engineer"` respectively.
2. `code-reviewer`: five-axis review across correctness, readability, architecture, security, and performance.
3. `security-auditor`: vulnerability and threat-model pass covering OWASP Top 10, secrets, auth/authz, and dependency CVEs.
4. `test-engineer`: coverage analysis for happy paths, edge cases, error paths, and concurrency scenarios.
5. Specialist personas do not call each other. They return reports to the main session only.
6. If subagents are unavailable, run the same persona prompts sequentially and treat their outputs as independent reports.

Phase B: merge in main context
1. Aggregate Critical and Important code quality findings and failing tests, lint, or build output.
2. Promote Critical or High security findings to launch blockers and cross-check with the review security axis.
3. Include performance risks and Core Web Vitals checks when applicable.
4. Verify accessibility directly: keyboard navigation, screen reader support, and contrast.
5. Verify infrastructure directly: env vars, migrations, monitoring, and feature flags.
6. Verify documentation directly: README, ADRs, changelog, and release notes as applicable.

Phase C: decision and rollback
1. Produce a single decision using this shape:

```markdown
## Ship Decision: GO | NO-GO

### Blockers (must fix before ship)
- [Source persona: Critical finding + file:line]

### Recommended fixes (should fix before ship)
- [Source persona: Important finding + file:line]

### Acknowledged risks (shipping anyway)
- [Risk + mitigation]

### Rollback plan
- Trigger conditions: [what signals would prompt rollback]
- Rollback procedure: [exact steps]
- Recovery time objective: [target]

### Specialist reports (full)
- [code-reviewer report]
- [security-auditor report]
- [test-engineer report]
```

2. Default to NO-GO for any Critical finding unless the user explicitly accepts the risk.
3. A rollback plan is mandatory before any GO recommendation.
