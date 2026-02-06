# Project Guidelines

This document summarizes the repository structure, tooling, and workflows.

## Structure

- `src/` for application code
- `tests/` for tests
- `scripts/` for helper scripts
- `docs/` for documentation
- `examples/` for usage examples
- `docker/` for Docker assets

## Tooling

- uv for environments and dependencies
- ruff for lint rules
- black for formatting
- flake8 for legacy lint checks
- mypy for type checking
- pytest for tests

## Workflows

GitHub Actions workflows live in `.github/workflows/`:

- `ci.yml` orchestrates lint, typecheck, tests, and build
- `ci-lint.yml` runs lint checks
- `ci-typecheck.yml` runs mypy
- `ci-tests.yml` runs tests on Linux, macOS, and Windows
- `ci-build.yml` builds distribution packages
- `ci-binary.yml` builds binaries
- `build-binaries.yml` triggers binary builds on tags
- `publish-to-pypi.yml` publishes to PyPI

## Release

1. Update version in `pyproject.toml` and `src/musiclist_for_soundiiz/__init__.py`.
2. Tag the release as `vX.Y.Z` and push the tag.
3. CI publishes packages and binaries.
