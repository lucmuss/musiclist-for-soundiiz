# MusicList for Soundiiz

[![CI](https://github.com/lucmuss/musiclist-for-soundiiz/workflows/CI/badge.svg)](https://github.com/lucmuss/musiclist-for-soundiiz/actions)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

Command-line and GUI tool for extracting music file metadata and creating playlists for Soundiiz import.

## Features

- Multi-format support: AAC, AU, FLAC, MP3, OGG, M4A, WAV, WMA
- Export formats: CSV (Soundiiz), JSON, M3U, TXT
- Recursive scanning and batch processing
- Duplicate detection and optional removal
- CLI and GUI interfaces

## Installation

### PyPI

```bash
uv pip install musiclist-for-soundiiz
```

### Docker

```bash
docker build -f docker/Dockerfile -t musiclist-for-soundiiz .

docker run --rm \
  -v /path/to/music:/music:ro \
  -v $(pwd)/output:/output \
  musiclist-for-soundiiz \
  -i /music -o /output/playlist.csv
```

See `docs/DOCKER.md` for details.

### From source (development)

```bash
git clone https://github.com/lucmuss/musiclist-for-soundiiz.git
cd musiclist-for-soundiiz

uv venv
uv sync --extra dev

uv run musiclist-for-soundiiz -i /path/to/music -o output.csv
uv run musiclist-for-soundiiz-gui
```

## Usage

### CLI

```bash
musiclist-for-soundiiz -i /music/library -o soundiiz.csv
musiclist-for-soundiiz -i /music -o playlist.json -f json
musiclist-for-soundiiz -i /music -o playlist.m3u -f m3u
musiclist-for-soundiiz -i /music -o playlist.txt -f txt
```

### GUI

```bash
musiclist-for-soundiiz-gui
```

## Development

This project uses uv, ruff, black, flake8, mypy, and pytest. The Justfile provides common tasks.

```bash
just setup
just format
just lint
just typecheck
just test
just ci
```

## Documentation

Documentation is in `docs/`.

- `docs/USAGE_EXAMPLES.md`
- `docs/DOCKER.md`
- `docs/TROUBLESHOOTING.md`
- `docs/GUI_QUICKSTART.md`
- `docs/GUI_INSTALLATION.md`
- `docs/BINARIES.md`
- `docs/PYPI_PUBLISH.md`
- `docs/CONTRIBUTING.md`
- `docs/PROJECT_GUIDELINES.md`
- `docs/SCREENSHOTS.md`

## Contributing

See `docs/CONTRIBUTING.md`.

## License

MIT. See `LICENSE`.
