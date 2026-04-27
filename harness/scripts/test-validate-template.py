#!/usr/bin/env python3
"""Smoke tests for harness/scripts/validate-template.py."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
VALIDATE_SCRIPT = REPO_ROOT / "harness/scripts/validate-template.py"


def load_validate_module():
    spec = importlib.util.spec_from_file_location("validate_template", VALIDATE_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {VALIDATE_SCRIPT}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


validate_template = load_validate_module()


class TemplateValidationTests(unittest.TestCase):
    def test_agents_entrypoint_size_allows_current_template(self) -> None:
        validate_template.validate_agents_entrypoint_size(validate_template.SOURCE_ROOT)
        validate_template.validate_agents_entrypoint_size(validate_template.OUTPUT_ROOT)

    def test_agents_entrypoint_size_rejects_over_limit(self) -> None:
        with tempfile.TemporaryDirectory(prefix="harness-validate-test.") as tmp:
            root = Path(tmp)
            lines = ["line"] * (validate_template.AGENTS_ENTRYPOINT_MAX_LINES + 1)
            (root / "AGENTS.md").write_text("\n".join(lines) + "\n")

            with self.assertRaises(SystemExit) as error:
                validate_template.validate_agents_entrypoint_size(root)

            self.assertIn("AGENTS.md has 201 lines", str(error.exception))
            self.assertIn("move details into docs/", str(error.exception))


if __name__ == "__main__":
    unittest.main()
