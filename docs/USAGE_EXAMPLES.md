# Usage Examples

## CLI Basics

```bash
musiclist-for-soundiiz -i /music/library -o soundiiz.csv
```

## Export Formats

```bash
musiclist-for-soundiiz -i /music -o playlist.csv -f csv
musiclist-for-soundiiz -i /music -o playlist.json -f json
musiclist-for-soundiiz -i /music -o playlist.m3u -f m3u
musiclist-for-soundiiz -i /music -o playlist.txt -f txt
```

## Duplicate Detection

```bash
musiclist-for-soundiiz -i /music -o output.csv --detect-duplicates
musiclist-for-soundiiz -i /music -o output.csv --remove-duplicates --strategy keep_first
```

## Non-Recursive Scan

```bash
musiclist-for-soundiiz -i /music --no-recursive -o output.csv
```

## GUI

```bash
musiclist-for-soundiiz-gui
```

## Docker

See `docs/DOCKER.md` for container usage.
