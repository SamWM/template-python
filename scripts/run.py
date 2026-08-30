#!/usr/bin/env python3
"""Cross-platform task runner for local development and build orchestration."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent


def get_uv_cmd() -> list[str]:
    """Get the appropriate uv command invocation."""
    if shutil.which("uv"):
        return ["uv"]
    return [sys.executable, "-m", "uv"]


def run_command(cmd: list[str], *, check: bool = True) -> int:
    """Execute a command in the project root directory."""
    if cmd and cmd[0] == "uv":
        cmd = get_uv_cmd() + cmd[1:]
    print(f"\n--> Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=ROOT_DIR)
    if check and result.returncode != 0:
        sys.exit(result.returncode)
    return result.returncode


def cmd_sync() -> None:
    """Sync virtual environment and install dev dependencies."""
    run_command(["uv", "sync", "--all-groups"])


def cmd_lint() -> None:
    """Run code linter and format checker."""
    run_command(["uv", "run", "ruff", "check", "."])
    run_command(["uv", "run", "ruff", "format", "--check", "."])


def cmd_format() -> None:
    """Format codebase and apply autofixes."""
    run_command(["uv", "run", "ruff", "format", "."])
    run_command(["uv", "run", "ruff", "check", "--fix", "."])


def cmd_typecheck() -> None:
    """Run pyright type checker."""
    run_command(["uv", "run", "pyright"])


def cmd_test() -> None:
    """Run test suite with coverage report."""
    run_command(["uv", "run", "pytest"])


def cmd_check() -> None:
    """Run all validation checks (lint, typecheck, test)."""
    print("\n=== [1/3] Running Linters & Format Checks ===")
    cmd_lint()
    print("\n=== [2/3] Running Type Checks ===")
    cmd_typecheck()
    print("\n=== [3/3] Running Test Suite ===")
    cmd_test()
    print("\n[SUCCESS] All checks passed successfully!")


def cmd_build() -> None:
    """Build distribution packages (wheel and sdist)."""
    run_command(["uv", "build"])


def cmd_clean() -> None:
    """Clean all build and temporary artifacts."""
    root_dirs = ["dist", "build", ".ruff_cache", ".pytest_cache", "htmlcov"]
    root_files = [".coverage", "coverage.xml"]

    print("\n--> Cleaning build and cache artifacts...")
    for d in root_dirs:
        target = ROOT_DIR / d
        if target.is_dir():
            shutil.rmtree(target, ignore_errors=True)
            print(f"Removed directory: {d}")

    for f in root_files:
        target = ROOT_DIR / f
        if target.is_file():
            target.unlink(missing_ok=True)
            print(f"Removed file: {f}")

    for egg_info in ROOT_DIR.glob("src/*.egg-info"):
        if egg_info.is_dir():
            shutil.rmtree(egg_info, ignore_errors=True)
            print(f"Removed directory: {egg_info.relative_to(ROOT_DIR)}")

    print("[SUCCESS] Workspace clean.")


def main() -> None:
    """Entrypoint for the task runner."""
    parser = argparse.ArgumentParser(
        description="Cross-platform task runner for Python project.",
    )
    parser.add_argument(
        "task",
        choices=[
            "sync",
            "lint",
            "format",
            "typecheck",
            "test",
            "check",
            "build",
            "clean",
        ],
        help="Task to execute",
    )

    args = parser.parse_args()

    task_map = {
        "sync": cmd_sync,
        "lint": cmd_lint,
        "format": cmd_format,
        "typecheck": cmd_typecheck,
        "test": cmd_test,
        "check": cmd_check,
        "build": cmd_build,
        "clean": cmd_clean,
    }

    task_map[args.task]()


if __name__ == "__main__":
    main()
