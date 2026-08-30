"""Modern PySide6 GUI interface for template-python."""

import sys
from collections.abc import Sequence

from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QKeySequence, QShortcut
from PySide6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from template_python import __version__
from template_python.core import greet


class GreetingWindow(QMainWindow):
    """Main application window for the Greeting GUI."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(f"template-python v{__version__}")
        self.setMinimumSize(460, 360)
        self._init_ui()
        self._update_greeting()

    def _init_ui(self) -> None:
        """Construct the UI widgets and layout."""
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(16)
        main_layout.setContentsMargins(24, 24, 24, 24)

        # Header
        header_label = QLabel("Greeting Generator", self)
        header_font = QFont()
        header_font.setPointSize(16)
        header_font.setBold(True)
        header_label.setFont(header_font)
        main_layout.addWidget(header_label)

        sub_label = QLabel(f"Cross-platform Python GUI Template (v{__version__})", self)
        sub_label.setStyleSheet("color: #666666;")
        main_layout.addWidget(sub_label)

        # Form Inputs
        inputs_layout = QVBoxLayout()
        inputs_layout.setSpacing(8)

        name_label = QLabel("Recipient Name:", self)
        inputs_layout.addWidget(name_label)

        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("World (default)")
        self.name_input.returnPressed.connect(self._on_greet_clicked)
        inputs_layout.addWidget(self.name_input)

        message_label = QLabel("Greeting Message Prefix:", self)
        inputs_layout.addWidget(message_label)

        self.message_input = QLineEdit(self)
        self.message_input.setPlaceholderText("Hello (default)")
        self.message_input.returnPressed.connect(self._on_greet_clicked)
        inputs_layout.addWidget(self.message_input)

        main_layout.addLayout(inputs_layout)

        # Action Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        self.greet_button = QPushButton("Greet", self)
        self.greet_button.setStyleSheet(
            "QPushButton { background-color: #0066cc; color: white; "
            "font-weight: bold; padding: 8px 16px; border-radius: 4px; } "
            "QPushButton:hover { background-color: #0052a3; }"
        )
        self.greet_button.clicked.connect(self._on_greet_clicked)
        button_layout.addWidget(self.greet_button)

        self.copy_button = QPushButton("Copy to Clipboard", self)
        self.copy_button.setStyleSheet("padding: 8px 16px;")
        self.copy_button.clicked.connect(self._on_copy_clicked)
        button_layout.addWidget(self.copy_button)

        main_layout.addLayout(button_layout)

        # Enter key shortcut to trigger Greet
        return_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Return), self)
        return_shortcut.activated.connect(self._on_greet_clicked)

        # Result Display Card
        result_card = QFrame(self)
        result_card.setFrameShape(QFrame.Shape.StyledPanel)
        result_card.setStyleSheet(
            "QFrame { background-color: #f4f6f8; border: 1px solid #dcdfe6; "
            "border-radius: 6px; padding: 12px; }"
        )
        result_layout = QVBoxLayout(result_card)

        self.result_label = QLabel(self)
        result_font = QFont()
        result_font.setPointSize(14)
        result_font.setBold(True)
        self.result_label.setFont(result_font)
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.result_label.setStyleSheet("color: #1a1a1a;")
        result_layout.addWidget(self.result_label)

        main_layout.addWidget(result_card)
        main_layout.addStretch()

        # Status Bar
        self.statusBar().showMessage("Ready")

    def _update_greeting(self) -> str:
        """Compute the greeting from input fields and update the result card."""
        name_text = self.name_input.text().strip() or "World"
        msg_text = self.message_input.text().strip() or "Hello"
        greeting = greet(name=name_text, custom_message=msg_text)
        formatted = greeting.format()
        self.result_label.setText(formatted)
        return formatted

    def _on_greet_clicked(self) -> None:
        """Handle Greet button click."""
        self._update_greeting()
        self.statusBar().showMessage("Greeting updated.", 3000)

    def _on_copy_clicked(self) -> None:
        """Copy formatted greeting to system clipboard."""
        formatted = self._update_greeting()
        clipboard = QApplication.clipboard()
        if clipboard is not None:
            clipboard.setText(formatted)
            self.statusBar().showMessage("Copied to clipboard!", 3000)


def main(argv: Sequence[str] | None = None) -> int:
    """GUI application entry point."""
    app = QApplication.instance()
    if app is None:
        app = QApplication(list(argv) if argv is not None else sys.argv)

    window = GreetingWindow()
    window.show()
    return int(app.exec())


if __name__ == "__main__":
    sys.exit(main())
