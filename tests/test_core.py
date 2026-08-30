"""Unit tests for template_python.core."""

import pytest

from template_python.core import Greeting, greet


def test_greet_defaults() -> None:
    """Test default greeting values."""
    res = greet()
    assert isinstance(res, Greeting)
    assert res.recipient == "World"
    assert res.message == "Hello"
    assert res.format() == "Hello, World!"


@pytest.mark.parametrize(
    ("name", "message", "expected"),
    [
        ("Alice", "Hi", "Hi, Alice!"),
        ("Bob", "Welcome", "Welcome, Bob!"),
        ("  Charlie  ", "  Good day  ", "Good day, Charlie!"),
        ("", "", "Hello, World!"),
    ],
)
def test_greet_custom(name: str, message: str, expected: str) -> None:
    """Test custom names and greeting messages."""
    res = greet(name=name, custom_message=message)
    assert res.format() == expected
