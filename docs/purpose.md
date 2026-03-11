# Project Purpose

**Qualitybase** is a Python library for code quality, development workflows, and project maintenance.

## Features

1. **quality** — Linting (ruff, mypy), security (bandit, pip-audit), complexity (radon), cleanup (vulture)
2. **build** — Package build
3. **clean** — Artifacts cleanup
4. **publish** — Publishing and distribution

## Architecture

- Built on [clicommands](https://github.com/octolo/python-clicommands) for the CLI
- Commands in `commands/`, discovered via `.commands.json`
- Entry point: `qualitybase` or `python -m qualitybase`

## Use Cases

- Standardized quality checks across multiple projects
- Consistent development workflows
- Vulnerability detection
- Project maintenance and cleanup
