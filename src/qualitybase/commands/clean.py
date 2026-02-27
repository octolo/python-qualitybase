"""Dev commands."""

from __future__ import annotations

import shutil
from pathlib import Path

from qualitybase.commands.args import parse_args_from_config
from qualitybase.commands.base import Command
from qualitybase.utils import print_header, print_info, print_separator, print_success

_ARG_CONFIG = {}


def _clean_build(root: Path) -> None:
    """Remove build artifacts in root."""
    for name in ["build", "dist", ".eggs"]:
        path = root / name
        if path.exists():
            shutil.rmtree(path, ignore_errors=True)
            print(f"  Removed {path}")
    for egg_info in root.glob("**/*.egg-info"):
        shutil.rmtree(egg_info, ignore_errors=True)
        print(f"  Removed {egg_info}")


def _clean_pyc(root: Path) -> None:
    """Remove Python bytecode artifacts in root."""
    for pycache in root.glob("**/__pycache__"):
        shutil.rmtree(pycache, ignore_errors=True)
        print(f"  Removed {pycache}")
    for pattern in ["**/*.pyc", "**/*.pyo", "**/*~"]:
        for file in root.glob(pattern):
            file.unlink(missing_ok=True)


def _clean_test(root: Path) -> None:
    """Remove test artifacts in root."""
    artifacts = [".pytest_cache", ".coverage", "htmlcov", ".mypy_cache", ".ruff_cache"]
    for name in artifacts:
        path = root / name
        if path.exists():
            if path.is_dir():
                shutil.rmtree(path, ignore_errors=True)
            else:
                path.unlink(missing_ok=True)
            print(f"  Removed {path}")


def _clean_directory(directory: str) -> None:
    """Clean one directory: build, bytecode, test artifacts."""
    root = Path(directory).resolve()
    if not root.exists():
        print_info(f"Skipping {directory}: not found")
        return
    print_info("Removing build artifacts...")
    _clean_build(root)
    print_info("Removing Python bytecode artifacts...")
    _clean_pyc(root)
    print_info("Removing test artifacts...")
    _clean_test(root)


def _clean_command(args: list[str]) -> bool:
    """Remove build, bytecode, and test artifacts in given directories."""
    parsed = parse_args_from_config(args, _ARG_CONFIG)
    directories = parsed.get("args", []) or ["."]
    for directory in directories:
        print_header(f"Clean: {directory}")
        print_separator()
        _clean_directory(directory)
        print_success("Done.")
    return True


clean_command = Command(_clean_command, "Remove build, bytecode, and test artifacts", inherit=False)
