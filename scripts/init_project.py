#!/usr/bin/env python3
"""Template initialization and renaming script.

Usage:
    uv run python scripts/init_project.py \\
        --name my-new-package \\
        --description "My project description" \\
        --author "Your Name" \\
        --email "you@example.com"
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent


def sanitize_package_name(name: str) -> tuple[str, str]:
    """Return (distribution_name, python_module_name)."""
    dist_name = name.strip().lower().replace("_", "-")
    module_name = dist_name.replace("-", "_")
    if not re.match(r"^[a-z][a-z0-9_]*$", module_name):
        raise ValueError(
            f"Invalid package name: {name}. Must start with a letter and "
            "contain only alphanumerics and hyphens/underscores."
        )
    return dist_name, module_name


def rename_project(
    dist_name: str,
    module_name: str,
    description: str,
    author: str,
    email: str,
) -> None:
    """Rename template files and update pyproject.toml."""
    pyproject_path = ROOT_DIR / "pyproject.toml"
    readme_path = ROOT_DIR / "README.md"
    src_dir = ROOT_DIR / "src"
    old_module_dir = src_dir / "template_python"
    new_module_dir = src_dir / module_name

    print(f"Initializing project: {dist_name} (module: {module_name})...")

    # Rename package directory in src/
    if old_module_dir.exists() and old_module_dir != new_module_dir:
        old_module_dir.rename(new_module_dir)
        print(f"Renamed module directory: src/template_python -> src/{module_name}")

    # Update pyproject.toml
    if pyproject_path.exists():
        content = pyproject_path.read_text(encoding="utf-8")
        content = re.sub(r'name = "template-python"', f'name = "{dist_name}"', content)
        content = re.sub(
            r'description = ".*?"', f'description = "{description}"', content
        )
        content = re.sub(r'name = "Your Name"', f'name = "{author}"', content)
        content = re.sub(r'email = "you@example.com"', f'email = "{email}"', content)
        content = re.sub(
            r'template-python = "template_python.cli:main"',
            f'{dist_name} = "{module_name}.cli:main"',
            content,
        )
        content = re.sub(
            r'packages = \["src/template_python"\]',
            f'packages = ["src/{module_name}"]',
            content,
        )
        content = re.sub(
            r'known-first-party = \["template_python"\]',
            f'known-first-party = ["{module_name}"]',
            content,
        )
        content = re.sub(
            r"--cov=template_python",
            f"--cov={module_name}",
            content,
        )
        content = re.sub(
            r'source = \["src/template_python"\]',
            f'source = ["src/{module_name}"]',
            content,
        )
        pyproject_path.write_text(content, encoding="utf-8")
        print("Updated pyproject.toml")

    # Update code references in python files
    for py_file in ROOT_DIR.glob("**/*.py"):
        if py_file.name == "init_project.py":
            continue
        code = py_file.read_text(encoding="utf-8")
        if "template_python" in code:
            code = code.replace("template_python", module_name)
            py_file.write_text(code, encoding="utf-8")
            print(f"Updated imports in {py_file.relative_to(ROOT_DIR)}")

    # Update README.md
    if readme_path.exists():
        readme_content = f"""# {dist_name}

{description}

## Quickstart

```bash
# Sync dependencies and create venv
uv sync

# Run tests
uv run pytest

# Run CLI
uv run {dist_name}
```
"""
        readme_path.write_text(readme_content, encoding="utf-8")
        print("Updated README.md")

    print("\n[SUCCESS] Project initialization complete!")


def main() -> None:
    """CLI entrypoint for init_project."""
    parser = argparse.ArgumentParser(description="Initialize project from template.")
    parser.add_argument(
        "--name", required=True, help="New package name (e.g. my-awesome-tool)"
    )
    parser.add_argument(
        "--description", default="Modern Python project", help="Project summary"
    )
    parser.add_argument("--author", default="Your Name", help="Author name")
    parser.add_argument("--email", default="you@example.com", help="Author email")

    args = parser.parse_args()

    try:
        dist_name, module_name = sanitize_package_name(args.name)
        rename_project(
            dist_name,
            module_name,
            args.description,
            args.author,
            args.email,
        )
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
