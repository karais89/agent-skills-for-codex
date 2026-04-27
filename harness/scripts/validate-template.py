#!/usr/bin/env python3
"""Validate the full harness template source and generated output."""

from __future__ import annotations

import json
import subprocess
import sys
import tomllib
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SOURCE_ROOT = REPO_ROOT / "harness/source/full/root"
OUTPUT_ROOT = REPO_ROOT / "harness/templates"
BUILD_SCRIPT = REPO_ROOT / "harness/scripts/build-template.py"
AGENTS_ENTRYPOINT_MAX_LINES = 200
FORBIDDEN_PATHS = [
    "SPEC.md",
    "tasks/plan.md",
    "tasks/todo.md",
    "docs/references",
]
LEGACY_WRAPPERS = [
    ".agents/skills/agent-skills-spec",
    ".agents/skills/agent-skills-plan",
    ".agents/skills/agent-skills-build",
]


def fail(message: str) -> None:
    raise SystemExit(message)


def parse_template_config(root: Path) -> None:
    json.loads((root / ".codex/hooks.json").read_text())
    tomllib.loads((root / ".codex/config.toml").read_text())
    for path in sorted((root / ".codex/agents").glob("*.toml")):
        data = tomllib.loads(path.read_text())
        for key in ("name", "description", "developer_instructions"):
            if key not in data:
                fail(f"{path.relative_to(root)} missing {key}")


def validate_skill_frontmatter(root: Path) -> int:
    count = 0
    for path in sorted((root / ".agents/skills").glob("*/SKILL.md")):
        text = path.read_text()
        if not text.startswith("---\n"):
            fail(f"{path.relative_to(root)} missing frontmatter")
        end = text.find("\n---\n", 4)
        if end == -1:
            fail(f"{path.relative_to(root)} has unclosed frontmatter")
        frontmatter = text[4:end]
        for key in ("name:", "description:"):
            if key not in frontmatter:
                fail(f"{path.relative_to(root)} missing {key}")
        count += 1
    if count == 0:
        fail(f"no skills found under {root}")
    return count


def validate_forbidden_paths(root: Path) -> None:
    for rel in FORBIDDEN_PATHS + LEGACY_WRAPPERS:
        if (root / rel).exists():
            fail(f"forbidden template path exists: {root.name}/{rel}")


def validate_no_reference_links(root: Path) -> None:
    needles = ("docs/references", "references/")
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        try:
            text = path.read_text()
        except UnicodeDecodeError:
            continue
        for needle in needles:
            if needle in text:
                fail(f"forbidden reference link {needle!r} in {path.relative_to(root)}")


def validate_agents_entrypoint_size(root: Path) -> None:
    path = root / "AGENTS.md"
    if not path.is_file():
        fail(f"template entrypoint missing: {path.relative_to(root)}")
    line_count = len(path.read_text().splitlines())
    if line_count > AGENTS_ENTRYPOINT_MAX_LINES:
        fail(
            f"AGENTS.md has {line_count} lines; keep it at or below "
            f"{AGENTS_ENTRYPOINT_MAX_LINES} lines and move details into docs/"
        )


def run_hook_checks(root: Path) -> None:
    user_hook = root / ".codex/hooks/user_prompt_submit.py"
    checks = [
        ("spec 새 기능 요구사항", "$harness-product-spec"),
        ("plan 사용자 설정 화면", "$harness-exec-plan"),
        ("build", "$harness-exec-build"),
    ]
    for prompt, expected in checks:
        proc = subprocess.run(
            [sys.executable, str(user_hook)],
            input=json.dumps({"prompt": prompt}),
            text=True,
            capture_output=True,
            check=True,
        )
        context = json.loads(proc.stdout)["hookSpecificOutput"].get("additionalContext", "")
        if expected not in context:
            fail(f"{prompt!r} did not map to {expected}")

    pre_hook = root / ".codex/hooks/pre_tool_use.py"
    proc = subprocess.run(
        [sys.executable, str(pre_hook)],
        input=json.dumps({"tool_input": {"cmd": "rm -rf .agents"}}),
        text=True,
        capture_output=True,
    )
    if proc.returncode != 2 or "blocked command" not in proc.stderr:
        fail("destructive command hook did not block rm -rf .agents")


def validate_tree(root: Path) -> int:
    if not root.is_dir():
        fail(f"template root not found: {root}")
    parse_template_config(root)
    skill_count = validate_skill_frontmatter(root)
    validate_forbidden_paths(root)
    validate_no_reference_links(root)
    validate_agents_entrypoint_size(root)
    run_hook_checks(root)
    return skill_count


def main() -> int:
    manifest = REPO_ROOT / "harness/source/full/manifest.toml"
    data = tomllib.loads(manifest.read_text())
    if data["template"]["source"] != "harness/source/full/root":
        fail("manifest source path mismatch")
    if data["template"]["output"] != "harness/templates":
        fail("manifest output path mismatch")
    if data["policy"]["distribution_model"] != "full":
        fail("manifest distribution model must be full")

    source_skills = validate_tree(SOURCE_ROOT)
    output_skills = validate_tree(OUTPUT_ROOT)
    if source_skills != output_skills:
        fail(f"source/output skill count mismatch: {source_skills} != {output_skills}")

    subprocess.run([sys.executable, str(BUILD_SCRIPT), "--check"], check=True)
    print("template validation ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
