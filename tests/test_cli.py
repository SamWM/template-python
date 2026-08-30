"""Unit tests for template_python.cli."""

import sys
from unittest.mock import MagicMock

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


def test_cli_gui_flag_success(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test template-python --gui launches GUI when PySide6 is installed."""
    mock_main = MagicMock(return_value=0)
    monkeypatch.setattr("template_python.gui.main", mock_main, raising=False)
    exit_code = main(["--gui"])
    assert exit_code == 0
    mock_main.assert_called_once()


def test_cli_gui_flag_missing_dependency(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    """Test template-python --gui reports clear error when PySide6 is missing."""
    monkeypatch.setitem(sys.modules, "template_python.gui", None)
    exit_code = main(["--gui"])
    assert exit_code == 1
    captured = capsys.readouterr()
    assert "Error: GUI dependencies are not installed." in captured.err
    assert "template-python[gui]" in captured.err
