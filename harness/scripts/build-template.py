#!/usr/bin/env python3
"""Build or compare the full harness template from its source tree."""

from __future__ import annotations

import argparse
import filecmp
import shutil
import sys
import tempfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SOURCE = REPO_ROOT / "harness/source/full/root"
DEFAULT_OUTPUT = REPO_ROOT / "harness/templates"


def relative_files(root: Path) -> dict[Path, Path]:
    files: dict[Path, Path] = {}
    for path in sorted(root.rglob("*")):
        if path.is_file() or path.is_symlink():
            files[path.relative_to(root)] = path
    return files


def copy_tree(source: Path, destination: Path) -> None:
    if not source.is_dir():
        raise SystemExit(f"source directory not found: {source}")
    if destination.exists():
        raise SystemExit(f"destination already exists: {destination}")
    shutil.copytree(source, destination, symlinks=True, copy_function=shutil.copy2)


def compare_trees(left: Path, right: Path) -> list[str]:
    problems: list[str] = []
    left_files = relative_files(left)
    right_files = relative_files(right)

    for rel in sorted(left_files.keys() - right_files.keys()):
        problems.append(f"missing from output: {rel}")
    for rel in sorted(right_files.keys() - left_files.keys()):
        problems.append(f"extra in output: {rel}")

    for rel in sorted(left_files.keys() & right_files.keys()):
        left_path = left_files[rel]
        right_path = right_files[rel]
        if left_path.is_symlink() or right_path.is_symlink():
            if not left_path.is_symlink() or not right_path.is_symlink():
                problems.append(f"symlink mismatch: {rel}")
            elif left_path.readlink() != right_path.readlink():
                problems.append(f"symlink target mismatch: {rel}")
            continue
        if not filecmp.cmp(left_path, right_path, shallow=False):
            problems.append(f"content differs: {rel}")
            continue
        left_exec = bool(left_path.stat().st_mode & 0o111)
        right_exec = bool(right_path.stat().st_mode & 0o111)
        if left_exec != right_exec:
            problems.append(f"executable bit differs: {rel}")

    return problems


def check(source: Path, output: Path) -> int:
    if not output.is_dir():
        raise SystemExit(f"output directory not found: {output}")
    with tempfile.TemporaryDirectory(prefix="harness-template-build.") as tmp:
        generated = Path(tmp) / "generated"
        copy_tree(source, generated)
        problems = compare_trees(generated, output)
    if problems:
        print("template drift detected:", file=sys.stderr)
        for problem in problems:
            print(f"- {problem}", file=sys.stderr)
        return 1
    print(f"template ok: {source.relative_to(REPO_ROOT)} matches {output.relative_to(REPO_ROOT)}")
    return 0


def generate(source: Path, destination: Path) -> int:
    copy_tree(source, destination)
    print(f"generated template: {destination}")
    return 0


def write(source: Path, output: Path) -> int:
    if output.resolve() == source.resolve():
        raise SystemExit("refusing to write output over source")
    if output.exists():
        shutil.rmtree(output)
    shutil.copytree(source, output, symlinks=True, copy_function=shutil.copy2)
    print(f"wrote template output: {output.relative_to(REPO_ROOT)}")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="compare source-generated output with harness/templates")
    mode.add_argument("--generate", type=Path, help="copy source into a new destination directory")
    mode.add_argument("--write", action="store_true", help="replace the output directory with source")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source = args.source.resolve()
    output = args.output.resolve()
    if args.generate:
        return generate(source, args.generate.resolve())
    if args.write:
        return write(source, output)
    return check(source, output)


if __name__ == "__main__":
    raise SystemExit(main())
