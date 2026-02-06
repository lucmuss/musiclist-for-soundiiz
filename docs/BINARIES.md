# Pre-built Binaries

Binaries are attached to GitHub releases when a tag `vX.Y.Z` is pushed.

## Download and Run

1. Download the ZIP for your platform from the latest release.
2. Extract the archive.
3. Run the CLI binary:

```bash
./musiclist-for-soundiiz -i /path/to/music -o output.csv
```

## Build Locally

```bash
uv venv
uv sync --extra dev
uv run --with pyinstaller python scripts/build_binary.py
```

## Notes

- The GUI binary is named `musiclist-for-soundiiz-gui`.
- See `docs/DOCKER.md` for container usage.
