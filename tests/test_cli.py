"""Unit tests for template_python.cli."""

import pytest

from template_python import __version__
from template_python.cli import main


def test_cli_default(capsys: pytest.CaptureFixture[str]) -> None:
    """Test CLI invocation with default arguments."""
    exit_code = main([])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out.strip() == "Hello, World!"


def test_cli_custom_arguments(capsys: pytest.CaptureFixture[str]) -> None:
    """Test CLI invocation with custom name and message flag."""
    exit_code = main(["Developer", "-m", "Greetings"])
    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out.strip() == "Greetings, Developer!"


def test_cli_version(capsys: pytest.CaptureFixture[str]) -> None:
    """Test CLI version flag."""
    with pytest.raises(SystemExit) as excinfo:
        main(["--version"])
    assert excinfo.value.code == 0
    captured = capsys.readouterr()
    assert __version__ in captured.out
