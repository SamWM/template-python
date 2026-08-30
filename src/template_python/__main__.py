"""Executable module entrypoint (python -m template_python)."""

import sys

from template_python.cli import main

if __name__ == "__main__":
    sys.exit(main())
