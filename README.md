# Python Project Template

A modern, fast, cross-platform Python project template powered by [uv](https://docs.astral.sh/uv/), [Ruff](https://docs.astral.sh/ruff/), [Pyright](https://github.com/microsoft/pyright), and [pytest](https://docs.pytest.org/).

## Features

- ⚡ **Blazing Fast Environment & Packaging**: Managed with `uv` (`.python-version`, `uv.lock`, PEP 517 `hatchling` builds).
- 🐍 **Modern Python Baseline**: Targeted for Python `>=3.12`.
- 🔍 **Ultra-Fast Linting & Formatting**: Configured with `ruff` for linting, code style, and imports.
- 🎯 **Strict Static Typing**: Configured with `pyright` for robust type checking.
- 🧪 **Comprehensive Testing**: `pytest` + `pytest-cov` with branch coverage.
- 🛠️ **Cross-Platform Task Runner**: Run commands seamlessly via `just` or `python scripts/run.py`.
- 🔄 **Quick Template Initializer**: Rename package and bootstrap metadata in one command with `scripts/init_project.py`.

---

## Directory Structure

```text
template-python/
├── .python-version             # Pinned Python version (3.12+)
├── .editorconfig               # Editor whitespace/formatting consistency
├── .gitignore                  # Standard Python gitignore
├── pyproject.toml              # Build config, dependencies, ruff, pyright & pytest settings
├── Justfile                    # Just task runner recipe file
├── README.md                   # Project documentation
├── src/
│   └── template_python/        # Source code (src layout)
│       ├── __init__.py
│       ├── __main__.py
│       ├── cli.py              # CLI entry point
│       └── core.py             # Core module logic
├── tests/                      # Pytest unit tests
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_cli.py
│   └── test_core.py
└── scripts/
    ├── run.py                  # Cross-platform fallback task runner
    └── init_project.py         # Project rename / bootstrap script
```

---

## Quickstart

### 1. Prerequisites

Make sure you have [uv](https://docs.astral.sh/uv/) installed:

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows PowerShell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Environment Setup

Clone this template and sync dependencies:

```bash
uv sync
```

`uv` will automatically download and install the required Python version if it's not already installed on your system.

---

## Common Development Tasks

You can use `just` or the built-in pure Python task runner `python scripts/run.py`:

| Action | With `just` | With `python scripts/run.py` | With direct `uv` |
| :--- | :--- | :--- | :--- |
| **Install / Sync venv** | `just install` | `python scripts/run.py sync` | `uv sync` |
| **Lint & Style Check** | `just lint` | `python scripts/run.py lint` | `uv run ruff check . && uv run ruff format --check .` |
| **Auto-Format Code** | `just format` | `python scripts/run.py format` | `uv run ruff format . && uv run ruff check --fix .` |
| **Type Check** | `just typecheck` | `python scripts/run.py typecheck`| `uv run pyright` |
| **Run Tests** | `just test` | `python scripts/run.py test` | `uv run pytest` |
| **Run All Quality Checks** | `just check` | `python scripts/run.py check` | *(Runs lint, typecheck, test)* |
| **Build Wheel & Sdist** | `just build` | `python scripts/run.py build` | `uv build` |
| **Clean Artifacts** | `just clean` | `python scripts/run.py clean` | *(Removes dist/, cache, coverage)* |
| **Run CLI Application** | `just run` | `uv run template-python` | `uv run template-python` |

---

## Initializing a New Project

To rename this template into your own project:

```bash
uv run python scripts/init_project.py --name "my-tool" --description "My awesome CLI tool" --author "Your Name" --email "you@example.com"
```

This will automatically rename the `src/template_python` directory, adjust imports, update `pyproject.toml`, and update `README.md`.
