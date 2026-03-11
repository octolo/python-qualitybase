"""Quality command."""

from __future__ import annotations

import subprocess

from clicommands.commands.args import parse_args_from_config
from clicommands.commands.base import Command
from clicommands.utils import print_header, print_separator, print_warning

_ARG_CONFIG = {
    "mode": {"type": str, "default": "lint"},
    "lint": {"type": str, "default": "ruff,mypy"},
    "cleanup": {"type": str, "default": "vulture"},
    "complexity": {"type": str, "default": "radon_cc,radon_mi,radon_raw"},
    "security": {"type": str, "default": "bandit,pip-audit"},
    "clean": {"type": "store_true"},
}


def _cmd_with_dir(cmd_template: list[str], directory: str) -> list[str]:
    """Replace path placeholder with directory."""
    return [directory if arg == "." else arg for arg in cmd_template]


_COMMANDS_CHECK = {
    "lint": {
        "ruff": ["ruff", "check", "."],
        "mypy": ["mypy", "."],
    },
    "cleanup": {
        "vulture": ["vulture", "--min-confidence", "80", "."],
    },
    "complexity": {
        "radon_cc": ["radon", "cc", ".", "-s", "-a"],
        "radon_mi": ["radon", "mi", ".", "-s"],
        "radon_raw": ["radon", "raw", ".", "-s"],
    },
    "security": {
        "bandit": ["bandit", "-r", "."],
        "pip-audit": ["pip-audit", "--skip-editable"],
    },
}

# Tools that audit env only, run once per invocation (not per directory)
_ENV_ONLY_LCCS = frozenset({"pip-audit"})


_COMMANDS_CLEAN = {
    "lint": {
        "ruff": ["ruff", "check", ".", "--fix"],
    },
}


def _clean_directory(directory: str, mode: str, lccs: str) -> None:
    mode_commands = _COMMANDS_CLEAN.get(mode) or {}
    cmd = mode_commands.get(lccs)
    if not cmd:
        print_warning(f"{mode} {lccs} can't clean")
        return
    subprocess.run(_cmd_with_dir(cmd, directory), check=False)


def _check_directory(directory: str, mode: str, lccs: str) -> None:
    mode_commands = _COMMANDS_CHECK.get(mode) or {}
    cmd = mode_commands.get(lccs)
    if not cmd:
        print_warning(f"{mode} {lccs} can't check")
        return
    subprocess.run(_cmd_with_dir(cmd, directory), check=False)


_MODES = ("lint", "cleanup", "complexity", "security")


def _quality_command(_args: list[str]) -> bool:
    """Quality command."""
    args = parse_args_from_config(_args, _ARG_CONFIG)
    raw_args = args.get("args", []) or []
    mode = args.get("mode")
    # If first positional is a mode name (e.g. "quality lint src"), use it
    if raw_args and raw_args[0] in _MODES and mode == _ARG_CONFIG["mode"]["default"]:
        mode = raw_args[0]
        raw_args = raw_args[1:]
    # If first arg is a known tool for this mode, use it as filter
    mode_commands = _COMMANDS_CHECK.get(mode) or {}
    lccs_filter = None
    if raw_args and raw_args[0] in mode_commands:
        lccs_filter = raw_args[0]
        raw_args = raw_args[1:]
    directories = raw_args if raw_args else ["."]
    lccs_list = [lccs_filter] if lccs_filter else args.get(mode).split(",")
    for directory in directories:
        for lccs in lccs_list:
            if lccs in _ENV_ONLY_LCCS and directory != directories[0]:
                continue  # pip-audit etc.: run once only
            print_header(
                f"Directory: {directory}, LCCS: {lccs}, Mode: {mode}, Clean: {args.get('clean')}"
            )
            print_separator()
            if args.get("clean"):
                _clean_directory(directory, mode, lccs)
            else:
                _check_directory(directory, mode, lccs)
    return True


quality_command = Command(_quality_command, "Quality command", inherit=False)
