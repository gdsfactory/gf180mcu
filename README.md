# gf180mcu 0.5.0

GlobalFoundries 180nm MCU based on [Google open source PDK](https://github.com/google/globalfoundries-pdk-libs-gf180mcu_fd_pr)

This is a pure python implementation of the PDK.

> **NOTE**: If you were previously using the `gf180` package, it has been renamed to `gf180mcu` and the original package is now deprecated. See the [migration guide](https://gdsfactory.github.io/gf180mcu/migration.html) for more information.

## Installation

We recommend `uv`

```bash
# On macOS and Linux.
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```bash
# On Windows.
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Installation for users

Use python 3.11, 3.12 or 3.13. We recommend [VSCode](https://code.visualstudio.com/) as an IDE.

```
uv pip install gf180mcu --upgrade
```

Then you need to restart Klayout to make sure the new technology installed appears.

### Installation for contributors

For developers you need to `git clone` the GitHub repository, fork it, git add, git commit, git push and merge request your changes.

```
git clone https://github.com/gdsfactory/gf180mcu.git
cd gf180
uv venv --python 3.12
uv sync --extra docs --extra dev
```

## Documentation

- [gdsfactory docs](https://gdsfactory.github.io/gdsfactory/)

## Pre-commit

```bash
make pre-commit
```

## Release

1. Update the changelog in `.changelog.d/` with entries describing the changes. Make sure the changelog is clear and readable for customers.
2. Bump the version:

```bash
tbump 0.0.1
```

3. Push the tag:

```bash
git push --tags
```

4. Create a pull request with the updated changelog and version bump. This triggers the release workflow that builds wheels and uploads them.
