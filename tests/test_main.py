"""Unit tests for template_python.__main__ execution."""

import subprocess
import sys


def test_main_module_execution() -> None:
    """Test running package as a module via python -m template_python."""
    result = subprocess.run(
        [sys.executable, "-m", "template_python", "Tester", "-m", "Welcome"],
        capture_output=True,
        text=True,
        check=True,
    )
    assert result.returncode == 0
    assert result.stdout.strip() == "Welcome, Tester!"
