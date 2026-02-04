#!/bin/bash
set -e

echo "Starting MusicList for Soundiiz..."

# Run the CLI application using uv
exec uv run python -m musiclist_for_soundiiz.cli "$@"
