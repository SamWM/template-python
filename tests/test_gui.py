"""Unit tests for the PySide6 GUI module."""

from typing import Any

import pytest
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication

from template_python import __version__
from template_python.gui import GreetingWindow, main


def test_greeting_window_initial_state(qtbot: Any) -> None:
    """Test initial UI state of GreetingWindow."""
    window = GreetingWindow()
    qtbot.addWidget(window)

    assert f"template-python v{__version__}" in window.windowTitle()
    assert window.name_input.text() == ""
    assert window.message_input.text() == ""
    assert window.result_label.text() == "Hello, World!"


def test_greeting_window_generate_custom_greeting(qtbot: Any) -> None:
    """Test clicking Greet button updates greeting result."""
    window = GreetingWindow()
    qtbot.addWidget(window)

    window.name_input.setText("Alice")
    window.message_input.setText("Welcome")
    qtbot.mouseClick(window.greet_button, Qt.MouseButton.LeftButton)

    assert window.result_label.text() == "Welcome, Alice!"
    assert window.statusBar().currentMessage() == "Greeting updated."


def test_greeting_window_copy_to_clipboard(qtbot: Any) -> None:
    """Test copy to clipboard button copies the formatted greeting."""
    window = GreetingWindow()
    qtbot.addWidget(window)

    window.name_input.setText("Bob")
    window.message_input.setText("Greetings")
    qtbot.mouseClick(window.greet_button, Qt.MouseButton.LeftButton)
    qtbot.mouseClick(window.copy_button, Qt.MouseButton.LeftButton)

    clipboard = QApplication.clipboard()
    assert clipboard is not None
    assert clipboard.text() == "Greetings, Bob!"
    assert window.statusBar().currentMessage() == "Copied to clipboard!"


def test_gui_main_headless(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that main() initializes QApplication and exits cleanly."""
    monkeypatch.setattr(GreetingWindow, "show", lambda self: None)
    monkeypatch.setattr(QApplication, "exec", lambda *args, **kwargs: 0)
    exit_code = main([])
    assert exit_code == 0
