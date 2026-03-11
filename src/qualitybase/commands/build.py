"""Build commands."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from clicommands.commands.args import parse_args_from_config
from clicommands.commands.base import Command
from clicommands.utils import print_header, print_info, print_separator, print_success

_ARG_CONFIG = {}


def _build_directory(directory: str) -> bool:
    """Build sdist and wheel for one directory."""
    root = Path(directory).resolve()
    if not root.exists():
        print_info(f"Skipping {directory}: not found")
        return False
    if not (root / "pyproject.toml").exists():
        print_info(f"Skipping {directory}: no pyproject.toml")
        return False
    print_info("Building package...")
    result = subprocess.run(
        [sys.executable, "-m", "build"],
        cwd=root,
        check=False,
    )
    if result.returncode != 0:
        return False
    print_success("Build complete. Artifacts in dist/")
    return True


def _build_command(args: list[str]) -> bool:
    """Build sdist and wheel for given directories."""
    parsed = parse_args_from_config(args, _ARG_CONFIG)
    directories = parsed.get("args", []) or ["."]
    ok = True
    for directory in directories:
        print_header(f"Build: {directory}")
        print_separator()
        if not _build_directory(directory):
            ok = False
    return ok


build_command = Command(
    _build_command, "Build sdist and wheel for given directories", inherit=False
)
