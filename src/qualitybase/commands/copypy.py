"""Copy Python file command."""

from __future__ import annotations

from pathlib import Path
from .base import Command
from qualitybase.commands.args import parse_args_from_config
from qualitybase.commands.base import Command
from qualitybase.utils import print_info, print_header, print_separator, print_warning


_COPY_PY = {
    "cli": "cli.py",
    "django": "django.py",
}

_ARG_CONFIG = {
    "file": {"type": str, "default": "service"},
}

def _copypy_command(_args: list[str]) -> bool:
    """Copy python file."""
    args = parse_args_from_config(_args, _ARG_CONFIG)
    pyfile = args.get("file")
    pyfile = _COPY_PY.get(pyfile)
    directories = args.get("args", [])
    if not pyfile:
        print_warning(f"File {pyfile} not found")
    else:
        for directory in directories:
            print_header(f"Directory: {directory}")
            print_separator()
            path = Path(directory) / pyfile
            if path.exists():
                print_info(f"Copying {pyfile} to {path}")
                #shutil.copy(pyfile, path)
            else:
                print_warning(f"File {pyfile} not found in {directory}")


copypy_command = Command(_copypy_command, "Copy python file", inherit=False)
