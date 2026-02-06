# Contributing

Thank you for contributing to MusicList for Soundiiz.

## Development Setup

```bash
uv venv
uv sync --extra dev
```

## Local Checks

```bash
just format
just lint
just typecheck
just test
just ci
```

## Git Workflow

- Branch naming:
  - `feature/short-description`
  - `bugfix/short-description`
  - `docs/short-description`
  - `release/x.y.z`
- Keep commits focused and descriptive.
- Open a pull request against `main` or `develop`.
- Ensure CI passes before requesting review.

## Release Process

- Update version in `pyproject.toml` and `src/musiclist_for_soundiiz/__init__.py`.
- Tag the release as `vX.Y.Z`.
- Push the tag to trigger publish and binary workflows.

## Code Standards

- Use ASCII-only text in code and docs.
- Keep documentation in `docs/`.
- Keep Python files under `src/`, `tests/`, or `scripts/`.

## Reporting Issues

Use GitHub issues with clear reproduction steps and environment details.
