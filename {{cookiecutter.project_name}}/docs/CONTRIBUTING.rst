## Contributing

# Setting up a development environment

You can set up a development environment by running:

```bash
python3 -m venv .env
source ./.env/bin/activate
pip install -v -e .[dev]
```

# Post setup

You should prepare pre-commit, which will help you by checking that commits
pass required checks:

```bash
pip install pre-commit # or brew install pre-commit on macOS
pre-commit install # Will install a pre-commit hook into the git repo
```

You can also/alternatively run `pre-commit run` (changes only) or
`pre-commit run --all-files` to check even without installing the hook.

# Testing

Use pytest to run the unit checks:

```bash
pytest
```
