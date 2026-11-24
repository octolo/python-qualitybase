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

## CI

CI checks installation on Python 3.12, Ruff, Bandit (medium/high confidence and
severity), runtime dependency advisories, and package builds. It warns until an
automated test suite is added.

## Documentation

- `docs/purpose.md` — Project purpose and goals
- `docs/structure.md` — Project structure
- `docs/development.md` — Development guidelines
- `docs/AI.md` — AI assistant contract

## CI packaging check

CI also installs the built wheel(s) in a clean environment and checks their
dependencies and imports without publishing. This installation check is
non-blocking during the initial rollout.

## Local audit

Install the project's development/test dependencies (including both local
packages where applicable), plus the audit tools:

```bash
python -m pip install ruff mypy bandit pip-audit vulture radon xenon pytest pytest-django pytest-cov build twine
make audit
```

Use the activated environment's Python, or pass `make audit PYTHON=/path/to/python`.
On systems without Make, run `python scripts/audit.py` directly. Git is required;
the geoaddress widget tests also require Node.js. The audit reports missing test
suites and runs all available checks even when earlier checks fail.
Xenon checks the absolute C, module B, and average A complexity thresholds. Existing
lint, typing, security, dependency, or test findings can make the audit fail.
CI also runs this audit as a non-blocking job and separately reports Radon maintainability without imposing a threshold.
