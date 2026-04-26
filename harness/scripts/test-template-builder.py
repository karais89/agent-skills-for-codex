#!/usr/bin/env python3
"""Smoke tests for harness/scripts/build-template.py."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
BUILD_SCRIPT = REPO_ROOT / "harness/scripts/build-template.py"


class TemplateBuilderTests(unittest.TestCase):
    def run_builder(self, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(BUILD_SCRIPT), *args],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=check,
        )

    def test_generate_and_check_external_output(self) -> None:
        with tempfile.TemporaryDirectory(prefix="harness-template-builder-test.") as tmp:
            generated = Path(tmp) / "generated"
            generate = self.run_builder("--generate", str(generated))
            self.assertIn("generated template:", generate.stdout)

            check = self.run_builder("--output", str(generated), "--check")
            self.assertIn("template ok:", check.stdout)

    def test_check_reports_extra_output_file(self) -> None:
        with tempfile.TemporaryDirectory(prefix="harness-template-builder-test.") as tmp:
            generated = Path(tmp) / "generated"
            self.run_builder("--generate", str(generated))
            (generated / "EXTRA_DRIFT_FILE").touch()

            check = self.run_builder("--output", str(generated), "--check", check=False)
            self.assertNotEqual(check.returncode, 0)
            self.assertIn("extra in output: EXTRA_DRIFT_FILE", check.stderr)


if __name__ == "__main__":
    unittest.main()
