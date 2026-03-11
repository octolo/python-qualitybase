# Project Structure

```
python-qualitybase/
├── src/qualitybase/
│   ├── __init__.py
│   ├── cli.py              # Entry point (clicommands.helpers.cli_main)
│   ├── commands/           # Qualitybase commands
│   │   ├── quality.py
│   │   ├── build.py
│   │   ├── clean.py
│   │   └── publish.py
│   └── .commands.json      # packages: [clicommands], directories: [commands]
├── tests/
├── docs/
├── pyproject.toml
└── README.md
```

### Key Files

- `cli.py`: Delegates to clicommands for command discovery and execution
- `commands/`: Implementations for quality, build, clean, publish
- `.commands.json`: Aggregates clicommands + quality commands
