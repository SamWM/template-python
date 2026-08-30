"""Command-line interface entry point."""

import argparse
import sys
from collections.abc import Sequence

from template_python import __version__
from template_python.core import greet


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser for CLI execution."""
    parser = argparse.ArgumentParser(
        prog="template-python",
        description="Modern cross-platform Python CLI template.",
    )
    parser.add_argument(
        "name",
        nargs="?",
        default="World",
        help="Name of the person or entity to greet (default: 'World')",
    )
    parser.add_argument(
        "-m",
        "--message",
        default="Hello",
        help="Custom greeting message prefix (default: 'Hello')",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """CLI execution entrypoint.

    Args:
        argv: Optional command-line argument list. Uses sys.argv if None.

    Returns:
        Exit code (0 for success).
    """
    parser = build_parser()
    args = parser.parse_args(argv if argv is not None else sys.argv[1:])

    greeting = greet(name=args.name, custom_message=args.message)
    print(greeting.format())
    return 0


if __name__ == "__main__":
    sys.exit(main())
