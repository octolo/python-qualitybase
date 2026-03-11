# python-qualitybase

Python library for code quality, development workflows, and project maintenance.

## Installation

```bash
pip install qualitybase
```

For development:

```bash
pip install -e .
pip install -e ".[dev,lint,quality,security,test]"
```

## Usage

Qualitybase exposes its commands via [clicommands](https://github.com/octolo/python-clicommands):

```bash
qualitybase <command> [args...]
```

### Commands

- **quality** — Quality checks (lint, security, test, complexity, cleanup)
- **build** — Package build
- **clean** — Build artifacts cleanup
- **publish** — Package publishing
- **version** — Show version (from clicommands)
- **copy** — Copy templates (from clicommands)
- **varenv** — Environment variables (from clicommands)

### Examples

```bash
# Quality (default: lint mode)
qualitybase quality
qualitybase quality --mode=security
qualitybase quality lint ruff

# Build and publish
qualitybase build
qualitybase publish

# Help
qualitybase
```

### Environment Variables

- **ENVFILE_PATH** — Path to `.env` file to load automatically

## Documentation

- `docs/purpose.md` — Project purpose and goals
- `docs/structure.md` — Project structure
- `docs/development.md` — Development guidelines
- `docs/AI.md` — AI assistant contract
