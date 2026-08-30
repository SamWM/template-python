# Justfile - Command runner for local development

set shell := ["bash", "-uc"]
set windows-shell := ["powershell.exe", "-NoLogo", "-Command"]

# Default recipe: list available commands
default:
    @just --list

# Install all project and development dependencies into local .venv
install:
    uv sync --all-groups

# Run ruff lint and format checks
lint:
    uv run ruff check .
    uv run ruff format --check .

# Automatically format code and fix lint issues
format:
    uv run ruff format .
    uv run ruff check --fix .

# Run Pyright static type checker
typecheck:
    uv run pyright

# Run test suite with code coverage
test:
    uv run pytest

# Run all quality checks (lint, typecheck, test)
check: lint typecheck test

# Build standard wheel and source distribution
build:
    uv build

# Clean temporary files and build artifacts
clean:
    uv run python scripts/run.py clean

# Run CLI application directly
run *ARGS:
    uv run template-python {{ARGS}}
