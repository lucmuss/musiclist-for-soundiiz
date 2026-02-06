# Docker Guide

The Docker image runs the CLI using uv inside the container.

## Build

```bash
docker build -f docker/Dockerfile -t musiclist-for-soundiiz .
```

## Run

```bash
docker run --rm \
  -v /path/to/music:/music:ro \
  -v $(pwd)/output:/output \
  musiclist-for-soundiiz \
  -i /music -o /output/playlist.csv
```

## Docker Compose

```bash
docker compose -f docker/docker-compose.yml run --rm musiclist \
  -i /music -o /output/playlist.csv
```

## Notes

- `/music` is read-only. `/output` is writable.
- Use CLI flags to change format, recursive scan, or duplicate handling.
