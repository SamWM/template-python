"""Core business logic for the template package."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Greeting:
    """Represents a greeting message."""

    recipient: str
    message: str

    def format(self) -> str:
        """Format the greeting string."""
        return f"{self.message}, {self.recipient}!"


def greet(name: str = "World", custom_message: str = "Hello") -> Greeting:
    """Generate a greeting object.

    Args:
        name: Name of the recipient.
        custom_message: Greeting prefix.

    Returns:
        A Greeting dataclass instance.
    """
    clean_name = name.strip() or "World"
    clean_message = custom_message.strip() or "Hello"
    return Greeting(recipient=clean_name, message=clean_message)
