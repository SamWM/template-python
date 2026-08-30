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
        "--gui",
        action="store_true",
        help="Launch the graphical user interface (GUI)",
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
        Exit code (0 for success, non-zero for error).
    """
    parser = build_parser()
    args = parser.parse_args(argv if argv is not None else sys.argv[1:])

    if args.gui:
        try:
            from template_python.gui import main as gui_main
        except ImportError:
            sys.stderr.write(
                "Error: GUI dependencies are not installed.\n"
                "To enable GUI support, install with the [gui] extra:\n"
                "  pip install template-python[gui]\n"
                "  uv sync --extra gui\n"
            )
            return 1
        return gui_main()

    greeting = greet(name=args.name, custom_message=args.message)
    print(greeting.format())
    return 0


if __name__ == "__main__":
    sys.exit(main())
