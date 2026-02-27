#!/usr/bin/env python3
"""Service router script for Python projects.

Routes commands to appropriate service scripts from qualitybase or local services.
Usage:
    ./service.py quality lint
    ./service.py dev install-dev
    ENSURE_VIRTUALENV=1 ./service.py dev help
"""

import sys
from pathlib import Path

from qualitybase.helpers.service import main

PROJECT_ROOT = Path(__file__).resolve().parent

if __name__ == "__main__":
    sys.exit(main(PROJECT_ROOT))
