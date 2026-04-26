#!/usr/bin/env python3
"""Smoke tests for harness/scripts/apply-template.py."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
APPLY_SCRIPT = REPO_ROOT / "harness/scripts/apply-template.py"
FORBIDDEN_PATHS = [
    "SPEC.md",
    "tasks/plan.md",
    "tasks/todo.md",
    "docs/references",
]


class TemplateApplyTests(unittest.TestCase):
    def run_apply(self, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(APPLY_SCRIPT), *args],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=check,
        )

    def assert_template_files_exist(self, target: Path) -> None:
        expected = [
            "AGENTS.md",
            "README.md",
            "ARCHITECTURE.md",
            ".codex/hooks.json",
            ".agents/skills/harness-product-spec/SKILL.md",
            "docs/exec-plans/active/.gitkeep",
            "docs/product-specs/template.md",
        ]
        for rel in expected:
            self.assertTrue((target / rel).exists(), rel)

    def assert_forbidden_paths_absent(self, target: Path) -> None:
        for rel in FORBIDDEN_PATHS:
            self.assertFalse((target / rel).exists(), rel)

    def test_apply_to_new_directory(self) -> None:
        with tempfile.TemporaryDirectory(prefix="harness-apply-test.") as tmp:
            target = Path(tmp) / "new-project"

            result = self.run_apply("--target", str(target))

            self.assertIn("apply complete", result.stdout)
            self.assert_template_files_exist(target)
            self.assert_forbidden_paths_absent(target)

    def test_apply_to_existing_git_project_keeps_git_directory(self) -> None:
        with tempfile.TemporaryDirectory(prefix="harness-apply-test.") as tmp:
            target = Path(tmp) / "existing-project"
            (target / ".git").mkdir(parents=True)
            (target / ".git/HEAD").write_text("ref: refs/heads/main\n")

            result = self.run_apply("--target", str(target))

            self.assertIn("apply complete", result.stdout)
            self.assertTrue((target / ".git/HEAD").exists())
            self.assert_template_files_exist(target)
            self.assert_forbidden_paths_absent(target)

    def test_dry_run_reports_without_writing(self) -> None:
        with tempfile.TemporaryDirectory(prefix="harness-apply-test.") as tmp:
            target = Path(tmp) / "dry-run-project"

            result = self.run_apply("--target", str(target), "--dry-run")

            self.assertIn("dry-run complete: no files written", result.stdout)
            self.assertFalse(target.exists())

    def test_reapply_identical_template_is_not_a_conflict(self) -> None:
        with tempfile.TemporaryDirectory(prefix="harness-apply-test.") as tmp:
            target = Path(tmp) / "existing-project"
            self.run_apply("--target", str(target))

            result = self.run_apply("--target", str(target))

            self.assertIn("conflicts: 0", result.stdout)
            self.assertIn("files to copy: 0", result.stdout)
            self.assertIn("apply complete", result.stdout)

    def test_conflict_aborts_without_partial_copy(self) -> None:
        with tempfile.TemporaryDirectory(prefix="harness-apply-test.") as tmp:
            target = Path(tmp) / "conflict-project"
            target.mkdir()
            (target / "AGENTS.md").write_text("existing project instructions\n")

            result = self.run_apply("--target", str(target), check=False)

            self.assertEqual(result.returncode, 1)
            self.assertIn("content conflict: AGENTS.md", result.stderr)
            self.assertEqual((target / "AGENTS.md").read_text(), "existing project instructions\n")
            self.assertFalse((target / ".codex").exists())
            self.assert_forbidden_paths_absent(target)


if __name__ == "__main__":
    unittest.main()
