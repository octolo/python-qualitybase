"""Help command for listing available commands."""

from __future__ import annotations

from qualitybase.helpers.cli import _CLI_CONTEXT, _discover_commands, _get_package_name_from_path

from .base import Command


def _help_command(_args: list[str]) -> bool:
    """Display available commands."""
    cli_path = _CLI_CONTEXT.get("cli_file_path")
    package_name = _get_package_name_from_path(cli_path) if cli_path else "unknown"
    commands = _discover_commands()

    print(f"Usage: {package_name} <command> [args...]")
    print("\nCommands:")
    for cmd_name, cmd_info in sorted(commands.items()):
        description = cmd_info.get("description", "")
        print(f"  {cmd_name:<12} {description}")
    print("\nExamples:")
    for cmd_name in list(commands.keys())[:3]:
        print(f"  {package_name} {cmd_name}")
    return True


help_command = Command(_help_command, "Display available commands")
