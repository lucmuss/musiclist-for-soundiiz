# MusicList for Soundiiz

[![CI](https://github.com/lucmuss/musiclist-for-soundiiz/workflows/CI/badge.svg)](https://github.com/lucmuss/musiclist-for-soundiiz/actions)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

Command-line, GUI, and **Web** tool for extracting music file metadata and creating playlists for Soundiiz import.

## Features

- **Multi-format support**: AAC, AU, FLAC, MP3, OGG, M4A, WAV, WMA
- **Export formats**: CSV (Soundiiz), JSON, M3U, TXT
- **Recursive scanning** and batch processing
- **Duplicate detection** and optional removal
- **Three interfaces**: CLI, GUI, and Web (NEW!)
- **Web Features**: User accounts, playlist management, drag & drop upload
- **Modern Web UI**: HTMX-powered, responsive design

## Quick Start

### CLI (Command Line)
```bash
musiclist-for-soundiiz -i /music/library -o soundiiz.csv
```

### GUI (Desktop)
```bash
musiclist-for-soundiiz-gui
```

### Web Interface (NEW!)
```bash
# Setup and start
just setup-web
just web-migrate
just web-dev

# Or use entrypoint directly
musiclist-for-soundiiz-web
```
Then open http://localhost:8000

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

### Web Interface 🌐

The web interface provides a modern, browser-based way to manage your music library and create playlists.

**Features:**
- Drag & drop music directory upload
- Automatic metadata extraction
- Playlist creation and management
- Export to all formats (CSV, JSON, M3U, TXT)
- User accounts with history
- Responsive design for mobile and desktop

**Quick Start:**
```bash
# 1. Setup web environment
just setup-web

# 2. Initialize database
just web-migrate

# 3. Create admin user (optional)
just web-createsuperuser

# 4. Start development server
just web-dev
```

**Production Deployment:**
```bash
# With Docker (includes PostgreSQL)
just docker-web-up

# Or manually
just web-production
```

**Entrypoint Options:**
```bash
musiclist-for-soundiiz-web                    # Development server
musiclist-for-soundiiz-web --port 8080       # Custom port
musiclist-for-soundiiz-web --production      # Production with gunicorn
musiclist-for-soundiiz-web --migrate         # Run migrations first
```

## Development

This project uses uv, ruff, mypy, and pytest. The Justfile provides common tasks.

### CLI/GUI Development
```bash
just setup
just bootstrap-env
ARGS='-i /path/to/music -o output.csv' just bootstrap-run
just format
just lint
just typecheck
just test
just ci
```

### Web Development
```bash
just setup-web      # Install web dependencies
just web-migrate    # Setup database
just web-dev        # Start development server
just web-test       # Run web tests
just web-test-cov   # Run tests with coverage
```

`just dev` delegates to `just bootstrap-run`.

### Available Just Commands
- `just setup` - Setup CLI environment
- `just setup-web` - Setup web environment
- `just web-dev` - Start web development server
- `just web-test` - Run web tests
- `just docker-web-up` - Start web with Docker
- `just ci` - Full CI pipeline

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
