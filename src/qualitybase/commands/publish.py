"""Publish commands."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from clicommands.commands.args import parse_args_from_config
from clicommands.commands.base import Command
from clicommands.utils import (
    print_header,
    print_info,
    print_separator,
    print_success,
    print_warning,
)

_ARG_CONFIG = {"mode": {"type": str, "default": "pip"}}


def _get_project_info(root: Path) -> dict[str, str | None]:
    """Parse version and name from pyproject.toml."""
    pyproject = root / "pyproject.toml"
    if not pyproject.exists():
        return {"version": None, "name": None}
    try:
        content = pyproject.read_text(encoding="utf-8")
    except OSError:
        return {"version": None, "name": None}
    version = None
    name = None
    in_project = False
    for line in content.split("\n"):
        stripped = line.strip()
        if stripped == "[project]":
            in_project = True
            continue
        if in_project and stripped.startswith("["):
            break
        if in_project and "=" in stripped:
            if stripped.startswith("version"):
                parts = stripped.split("=", 1)
                version = parts[1].strip().strip('"').strip("'")
            elif stripped.startswith("name"):
                parts = stripped.split("=", 1)
                name = parts[1].strip().strip('"').strip("'")
    return {"version": version, "name": name}


def _read_release_notes(root: Path, version: str, tag: str) -> str:
    """Read release notes from CHANGELOG.md."""
    changelog = root / "CHANGELOG.md"
    if not changelog.exists():
        return f"Release {version}"
    try:
        content = changelog.read_text(encoding="utf-8")
    except OSError:
        return f"Release {version}"
    start = content.find(f"## {version}")
    if start == -1:
        start = content.find(f"## {tag}")
    if start == -1:
        return f"Release {version}"
    end = content.find("## ", start + 1)
    if end == -1:
        return content[start:].strip()
    return content[start:end].strip()


def _publish_pip(root: Path) -> bool:
    """Build and upload to PyPI."""
    info = _get_project_info(root)
    if not info.get("version"):
        print_warning("Could not determine version from pyproject.toml")
        return False

    # Build
    print_info("Building package...")
    r = subprocess.run([sys.executable, "-m", "build"], cwd=root, check=False)
    if r.returncode != 0:
        return False
    print_success("Build complete.")

    # Confirmation
    print_warning("WARNING: This will upload to PyPI!")
    print_warning("  1. Updated version in pyproject.toml")
    print_warning("  2. Updated CHANGELOG.md")
    print_warning("  3. Run all tests and quality checks")
    try:
        input("Press Enter to continue, or Ctrl+C to cancel... ")
    except KeyboardInterrupt:
        return False

    # Install twine, upload
    print_info("Uploading to PyPI...")
    r = subprocess.run(
        [sys.executable, "-m", "pip", "install", "--upgrade", "twine"],
        cwd=root,
        check=False,
    )
    if r.returncode != 0:
        return False
    r = subprocess.run(
        [sys.executable, "-m", "twine", "upload", "dist/*"], cwd=root, check=False
    )
    if r.returncode != 0:
        return False
    print_success("Upload to PyPI complete!")
    name = info.get("name") or root.name
    print_info(f"Install with: pip install {name}=={info['version']}")
    return True


def _publish_github(root: Path) -> bool:
    """Create GitHub release."""
    info = _get_project_info(root)
    version = info.get("version")
    if not version:
        print_warning("Could not determine version from pyproject.toml")
        return False

    tag = f"v{version}"
    # Check gh CLI
    r = subprocess.run(["gh", "--version"], capture_output=True, text=True, check=False)
    if r.returncode != 0:
        print_warning("GitHub CLI (gh) not found. Install: https://cli.github.com/")
        return False

    print_info(f"Creating GitHub release for {tag}...")
    notes = _read_release_notes(root, version, tag)
    r = subprocess.run(
        [
            "gh",
            "release",
            "create",
            tag,
            "--title",
            f"Release {version}",
            "--notes",
            notes,
        ],
        cwd=root,
        check=False,
    )
    if r.returncode != 0:
        return False
    print_success(f"GitHub release created: {tag}")
    return True


def _publish_directory(directory: str, mode: str) -> bool:
    """Publish one directory: pip (PyPI) or github (release)."""
    root = Path(directory).resolve()
    if not root.exists():
        print_info(f"Skipping {directory}: not found")
        return False
    if not (root / "pyproject.toml").exists():
        print_info(f"Skipping {directory}: no pyproject.toml")
        return False
    if mode == "pip":
        return _publish_pip(root)
    if mode == "github":
        return _publish_github(root)
    print_info(f"Unknown mode: {mode}. Use pip or github.")
    return False


def _publish_command(args: list[str]) -> bool:
    """Publish to PyPI (pip) or create GitHub release (github)."""
    parsed = parse_args_from_config(args, _ARG_CONFIG)
    unknowns = parsed.get("args", [])
    if "--help" in unknowns or "-h" in unknowns:
        print_info("Usage: qualitybase publish [--mode pip|github] [dir...]")
        print_info("  --mode pip     Upload to PyPI (default)")
        print_info("  --mode github  Create GitHub release")
        print_info("  dir            Directory(ies) with pyproject.toml (default: .)")
        return True
    mode = (parsed.get("mode") or "pip").lower()
    directories = [a for a in unknowns if not a.startswith("-")]
    if not directories:
        directories = ["."]
    ok = True
    for directory in directories:
        print_header(f"Publish [{mode}]: {directory}")
        print_separator()
        if not _publish_directory(directory, mode):
            ok = False
    return ok


publish_command = Command(
    _publish_command,
    "Publish to PyPI (pip) or GitHub (github)",
    inherit=False,
)
