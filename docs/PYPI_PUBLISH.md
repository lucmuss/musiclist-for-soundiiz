# PyPI Publishing

Publishing is automated by GitHub Actions in `publish-to-pypi.yml`.

## Release Tags

1. Update version in `pyproject.toml` and `src/musiclist_for_soundiiz/__init__.py`.
2. Commit the changes.
3. Tag the commit:

```bash
git tag vX.Y.Z
git push origin vX.Y.Z
```

The workflow builds the package and publishes to PyPI.

## Manual Publish

The workflow supports `workflow_dispatch` with a `publish_target` input:

- `pypi`
- `testpypi`

## Secrets

- `PYPI_API_TOKEN` for PyPI
- `TEST_PYPI_API_TOKEN` for TestPyPI
