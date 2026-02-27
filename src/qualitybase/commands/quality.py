"""Quality command."""

from __future__ import annotations

import subprocess

from qualitybase.commands.args import parse_args_from_config
from qualitybase.commands.base import Command
from qualitybase.utils import print_header, print_separator, print_warning

_ARG_CONFIG = {
    "mode": {"type": str, "default": "lint"},
    "lint": {"type": str, "default": "ruff,mypy,pylint,semgrep"},
    "cleanup": {"type": str, "default": "vulture,autoflake,pylint"},
    "complexity": {"type": str, "default": "radon_cc,radon_mi,radon_raw"},
    "security": {"type": str, "default": "bandit,safety,pip_audit,semgrep"},
    "clean": {"type": "store_true"},
}

def _cmd_with_dir(cmd_template: list[str], directory: str) -> list[str]:
    """Replace path placeholder with directory."""
    return [directory if arg == "." else arg for arg in cmd_template]


_COMMANDS_CHECK = {
    "lint": {
        "ruff": ["ruff", "check", "."],
        "mypy": ["mypy", "."],
        "pylint": ["pylint", "--ignore=.venv,.git,__pycache__,.mypy_cache", "."],
        "semgrep": ["semgrep", "."],
    },
    "cleanup": {
        "vulture": ["vulture", "--min-confidence", "80", "."],
        "autoflake": [
            "autoflake",
            "--check",
            "--recursive",
            "--remove-all-unused-imports",
            "--remove-unused-variables",
            ".",
        ],
        "pylint": ["pylint", "--ignore=.venv,.git,__pycache__,.mypy_cache", "."],
    },
    "complexity": {
        "radon_cc": ["radon", "cc", ".", "-s", "-a"],
        "radon_mi": ["radon", "mi", ".", "-s"],
        "radon_raw": ["radon", "raw", ".", "-s"],
    },
    "security": {
        "bandit": ["bandit"],
        "safety": ["safety"],
        "pip_audit": ["pip_audit"],
        "semgrep": ["semgrep"],
    },
}


_COMMANDS_CLEAN = {
    "lint": {
        "ruff": ["ruff", "check", ".", "--fix"],
        "semgrep": ["semgrep", ".", "--autofix"],
    },
    "cleanup": {
        "autoflake": [
            "autoflake",
            "--in-place",
            "--recursive",
            "--remove-all-unused-imports",
            "--remove-unused-variables",
            ".",
        ],
    },
}


def _clean_directory(directory: str, mode: str, lccs: str) -> None:
    cmd = _COMMANDS_CLEAN.get(mode).get(lccs)
    if not cmd:
        print_warning(f"{mode} {lccs} can't clean")
        return
    subprocess.run(_cmd_with_dir(cmd, directory), check=False)


def _check_directory(directory: str, mode: str, lccs: str) -> None:
    cmd = _COMMANDS_CHECK.get(mode).get(lccs)
    if not cmd:
        print_warning(f"{mode} {lccs} can't check")
        return
    subprocess.run(_cmd_with_dir(cmd, directory), check=False)


def _quality_command(_args: list[str]) -> bool:
    """Quality command."""
    args = parse_args_from_config(_args, _ARG_CONFIG)
    directories = args.get("args", []) or ["."]
    mode = args.get("mode")
    for directory in directories:
        for lccs in args.get(mode).split(","):
            print_header(f"Directory: {directory}, LCCS: {lccs}, Mode: {mode}, Clean: {args.get('clean')}")
            print_separator()
            if args.get("clean"):
                _clean_directory(directory, mode, lccs)
            else:
                _check_directory(directory, mode, lccs)
    return True


quality_command = Command(_quality_command, "Quality command", inherit=False)
