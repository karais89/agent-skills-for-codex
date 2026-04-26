#!/usr/bin/env python3
"""Apply the full harness template to a target project without overwriting conflicts."""

from __future__ import annotations

import argparse
import filecmp
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SOURCE = REPO_ROOT / "harness/templates"
FORBIDDEN_TEMPLATE_PATHS = [
    Path("SPEC.md"),
    Path("tasks/plan.md"),
    Path("tasks/todo.md"),
    Path("docs/references"),
]


@dataclass
class ApplyPlan:
    directories: list[Path]
    files_to_copy: list[Path]
    identical_files: list[Path]
    conflicts: list[str]


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def path_is_relative_to(path: Path, base: Path) -> bool:
    try:
        path.relative_to(base)
    except ValueError:
        return False
    return True


def relative_entries(root: Path) -> tuple[list[Path], list[Path]]:
    directories: list[Path] = []
    files: list[Path] = []
    for path in sorted(root.rglob("*")):
        rel = path.relative_to(root)
        if path.is_dir():
            directories.append(rel)
        elif path.is_file() or path.is_symlink():
            files.append(rel)
    return directories, files


def validate_source(source: Path) -> None:
    if not source.is_dir():
        raise SystemExit(f"template source not found: {source}")
    for rel in FORBIDDEN_TEMPLATE_PATHS:
        if (source / rel).exists():
            raise SystemExit(f"forbidden template path exists: {rel}")


def validate_target(source: Path, target: Path) -> None:
    if target.exists() and not target.is_dir():
        raise SystemExit(f"target exists but is not a directory: {target}")
    if source == target:
        raise SystemExit("refusing to apply template to the source directory itself")
    if path_is_relative_to(target, source):
        raise SystemExit("refusing to apply template inside the source directory")


def symlink_matches(source: Path, target: Path) -> bool:
    return target.is_symlink() and source.readlink() == target.readlink()


def file_matches(source: Path, target: Path) -> bool:
    if not target.is_file() or target.is_symlink():
        return False
    if not filecmp.cmp(source, target, shallow=False):
        return False
    source_exec = bool(source.stat().st_mode & 0o111)
    target_exec = bool(target.stat().st_mode & 0o111)
    return source_exec == target_exec


def build_apply_plan(source: Path, target: Path) -> ApplyPlan:
    directories, files = relative_entries(source)
    conflicts: list[str] = []
    files_to_copy: list[Path] = []
    identical_files: list[Path] = []

    if target.exists():
        for rel in directories:
            target_path = target / rel
            if target_path.exists() and not target_path.is_dir():
                conflicts.append(f"type conflict, expected directory: {rel}")

    for rel in files:
        source_path = source / rel
        target_path = target / rel
        if not target_path.exists() and not target_path.is_symlink():
            files_to_copy.append(rel)
            continue

        if source_path.is_symlink():
            if symlink_matches(source_path, target_path):
                identical_files.append(rel)
            else:
                conflicts.append(f"symlink conflict: {rel}")
            continue

        if file_matches(source_path, target_path):
            identical_files.append(rel)
            continue

        if target_path.is_dir():
            conflicts.append(f"type conflict, expected file: {rel}")
        else:
            conflicts.append(f"content conflict: {rel}")

    return ApplyPlan(
        directories=directories,
        files_to_copy=files_to_copy,
        identical_files=identical_files,
        conflicts=conflicts,
    )


def copy_file(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    if source.is_symlink():
        target.symlink_to(source.readlink())
        return
    shutil.copy2(source, target)


def apply_plan(source: Path, target: Path, plan: ApplyPlan, dry_run: bool) -> None:
    if dry_run:
        return
    target.mkdir(parents=True, exist_ok=True)
    for rel in plan.directories:
        (target / rel).mkdir(parents=True, exist_ok=True)
    for rel in plan.files_to_copy:
        copy_file(source / rel, target / rel)


def print_plan(source: Path, target: Path, plan: ApplyPlan, dry_run: bool) -> None:
    action = "dry-run" if dry_run else "apply"
    print(f"harness {action}: {display_path(source)} -> {target}")
    print(f"files to copy: {len(plan.files_to_copy)}")
    print(f"identical files: {len(plan.identical_files)}")
    print(f"conflicts: {len(plan.conflicts)}")

    if plan.conflicts:
        print("conflicting paths:", file=sys.stderr)
        for conflict in plan.conflicts:
            print(f"- {conflict}", file=sys.stderr)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True, type=Path, help="target project root")
    parser.add_argument("--source", default=DEFAULT_SOURCE, type=Path, help="template root to apply")
    parser.add_argument("--dry-run", action="store_true", help="report the apply plan without writing files")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    source = args.source.resolve()
    target = args.target.resolve()

    validate_source(source)
    validate_target(source, target)

    plan = build_apply_plan(source, target)
    print_plan(source, target, plan, args.dry_run)

    if plan.conflicts:
        return 1

    apply_plan(source, target, plan, args.dry_run)
    if args.dry_run:
        print("dry-run complete: no files written")
    else:
        print("apply complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
