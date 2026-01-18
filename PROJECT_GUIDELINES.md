# Project Guidelines & Best Practices

Comprehensive documentation of project structure, workflows, and development preferences for MusicList for Soundiiz. This document serves as a blueprint for maintaining consistency across similar projects.

---

## 📋 Table of Contents

- [Project Philosophy](#project-philosophy)
- [Repository Structure](#repository-structure)
- [Code Organization](#code-organization)
- [Documentation Standards](#documentation-standards)
- [CI/CD Workflows](#cicd-workflows)
- [Testing Strategy](#testing-strategy)
- [Release Management](#release-management)
- [Package Distribution](#package-distribution)
- [Development Workflow](#development-workflow)
- [Code Style & Quality](#code-style--quality)

---

## Project Philosophy

### Core Principles

1. **Production-Ready First** - Every feature should be fully tested and documented before release
2. **Multiple Installation Methods** - Support Homebrew, PyPI, Docker, and from-source installations
3. **Comprehensive Documentation** - Separate guides for different use cases and audiences
4. **Automated Everything** - CI/CD for testing, building, and publishing
5. **User-Friendly** - Both GUI and CLI interfaces with clear error messages
6. **Cross-Platform** - Works on macOS, Linux, and Windows
7. **Professional Structure** - Well-organized, scalable, and maintainable codebase

### Target Audiences

- **End Users**: GUI application with no technical knowledge required
- **Power Users**: CLI with extensive options and scripting support
- **Developers**: Clean API, extensive tests, clear contribution guidelines
- **DevOps**: Docker support for containerized deployments

---

## Repository Structure

### Standard Layout

```
project-name/
├── .github/                        # GitHub-specific files
│   └── workflows/                  # GitHub Actions workflows
│       ├── ci.yml                  # Continuous Integration
│       ├── build-binaries.yml      # Cross-platform binary builds
│       └── publish-to-pypi.yml     # PyPI publication
│
├── src/                            # Source code (importable package)
│   └── package_name/
│       ├── __init__.py             # Package initialization & version
│       ├── cli.py                  # Command-line interface
│       ├── gui.py                  # Graphical user interface
│       ├── core_module.py          # Core functionality
│       ├── utils.py                # Utility functions
│       └── i18n.py                 # Internationalization (if needed)
│
├── tests/                          # Test suite
│   ├── __init__.py
│   ├── README.md                   # Test documentation
│   ├── test_*.py                   # Test files
│   ├── test_integration.py         # Integration tests
│   └── fixtures/                   # Test data
│
├── docs/                           # Extended documentation
│   ├── SCREENSHOTS.md              # Visual guides
│   ├── USAGE_EXAMPLES.md           # Detailed examples
│   ├── TROUBLESHOOTING.md          # Common problems & solutions
│   └── images/                     # Screenshots and diagrams
│
├── examples/                       # Usage examples
│   └── example_usage.sh
│
├── Formula/                        # Homebrew formula
│   └── package-name.rb
│
├── build/                          # Build artifacts (gitignored)
├── dist/                           # Distribution files (gitignored)
│
├── .dockerignore                   # Docker ignore patterns
├── .gitignore                      # Git ignore patterns
├── Dockerfile                      # Docker image definition
├── docker-compose.yml              # Docker Compose configuration
│
├── setup.py                        # Python package setup (legacy)
├── pyproject.toml                  # Modern Python packaging
├── MANIFEST.in                     # Package file inclusion rules
├── requirements.txt                # Production dependencies
├── requirements-dev.txt            # Development dependencies
│
├── mypy.ini                        # Type checking configuration
├── build_binary.py                 # Binary building script
├── cli_entrypoint.py               # CLI entry point script
├── gui_entrypoint.py               # GUI entry point script
│
├── README.md                       # Main project documentation
├── CONTRIBUTING.md                 # Contribution guidelines
├── LICENSE                         # License file (MIT)
├── BINARIES.md                     # Binary usage guide
├── DOCKER.md                       # Docker usage guide
├── HOMEBREW.md                     # Homebrew publication guide
├── PYPI_PUBLISH.md                 # PyPI publication guide
├── GUI_INSTALLATION.md             # GUI setup instructions
├── GUI_QUICKSTART.md               # GUI quick start
└── PROJECT_GUIDELINES.md           # This file
```

### Key Structural Decisions

#### 1. Source in `src/` Directory

```
src/package_name/        # ✅ Preferred
package_name/            # ❌ Avoid
```

**Why?**
- Prevents accidental imports from project root
- Clear separation of source code and project files
- Better for testing and packaging

#### 2. Separate Test Directory

```
tests/                   # ✅ At project root
src/package_name/tests/  # ❌ Avoid
```

**Why?**
- Tests are not part of the distributed package
- Easier to run all tests
- Clear boundary between code and tests

#### 3. Documentation Structure

```
README.md               # High-level overview, quick start
docs/                   # Detailed guides
  ├── USAGE_EXAMPLES.md
  ├── TROUBLESHOOTING.md
  └── SCREENSHOTS.md
CONTRIBUTING.md         # How to contribute
DOCKER.md              # Docker-specific guide
PYPI_PUBLISH.md        # Publishing guide
```

**Why?**
- README stays concise and approachable
- Specialized guides for different needs
- Easy to navigate and maintain

---

## Code Organization

### Module Responsibilities

```python
# __init__.py - Package initialization
"""Package description."""
__version__ = "1.0.6"
__author__ = "Author Name"
__license__ = "MIT"

from .cli import main
from .core import CoreClass

__all__ = ["main", "CoreClass"]
```

```python
# cli.py - Command-line interface only
import argparse
from .core import CoreClass

def main():
    parser = argparse.ArgumentParser()
    # CLI logic only
```

```python
# gui.py - Graphical interface only
import tkinter as tk
from .core import CoreClass

def main():
    # GUI logic only
```

```python
# core.py - Business logic (no UI)
class CoreClass:
    """Core functionality usable by CLI, GUI, or as library."""
    def process(self):
        # Pure logic, no print() or UI code
```

### Separation of Concerns

```python
# ✅ Good: Separate concerns
class MusicExtractor:
    """Extracts metadata from music files."""
    def extract(self, file_path):
        return metadata

class CSVExporter:
    """Exports data to CSV format."""
    def export(self, data, output_path):
        # Write CSV

# ❌ Bad: Mixed concerns
class MusicProcessor:
    def process_and_export(self, file_path, output_path):
        # Extraction + Export + CLI output mixed
```

### Internationalization Pattern

```python
# i18n.py - Translation system
TRANSLATIONS = {
    "en": {"greeting": "Hello"},
    "de": {"greeting": "Hallo"},
    # ...
}

def get_text(key, lang="en"):
    return TRANSLATIONS.get(lang, {}).get(key, key)

# Usage in GUI
from .i18n import get_text

class App:
    def __init__(self, language="en"):
        self.t = lambda key: get_text(key, language)
        button_text = self.t("process_files")
```

---

## Documentation Standards

### README.md Structure

```markdown
# Project Name 🎵

[Badges: CI, Python version, License, Code style]

Brief description (1-2 sentences)

## ✨ Features
- Feature 1
- Feature 2

## 📋 Table of Contents
- Installation
- Quick Start
- Usage
- ...

## 🚀 Installation

### Option 1: Homebrew (Recommended)
### Option 2: PyPI
### Option 3: Docker
### Option 4: From Source

## ⚡ Quick Start

### GUI Version
### CLI Version

## 📚 Usage Examples
[Basic examples]

## ⚙️ Configuration
[Options table]

## 🧪 Testing
## 🤝 Contributing
## 📝 License
```

### Separate Documentation Files

1. **USAGE_EXAMPLES.md**
   - 15-20 detailed examples
   - Organized by complexity
   - Real-world scenarios
   - Code snippets with outputs

2. **TROUBLESHOOTING.md**
   - Common errors with solutions
   - Platform-specific issues
   - Performance tips
   - Debug instructions

3. **SCREENSHOTS.md**
   - Visual guides
   - Screenshot placeholders
   - Instructions for creating screenshots
   - Consistent styling guidelines

4. **DOCKER.md**
   - Complete Docker guide
   - docker-compose examples
   - Volume mounting patterns
   - Platform-specific commands

5. **PYPI_PUBLISH.md**
   - Step-by-step publishing guide
   - Manual and automated methods
   - Version management
   - Troubleshooting

6. **HOMEBREW.md**
   - Tap creation guide
   - Formula template
   - Testing instructions
   - Update procedures

### Code Comments

```python
# ✅ Good: Explain WHY, not WHAT
def parse_filename(filename):
    """
    Parse filename to extract artist and title.
    
    Handles "Artist - Title" format commonly used when
    metadata tags are missing or incomplete.
    """
    # Split only on first dash to handle titles with dashes
    parts = filename.rsplit(" - ", 1)
    return parts

# ❌ Bad: Obvious comments
def parse_filename(filename):
    # Split the filename  (obvious)
    parts = filename.split(" - ")
    # Return the parts  (obvious)
    return parts
```

---

## CI/CD Workflows

### GitHub Actions Structure

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    strategy:
      matrix:
        os: [ubuntu-latest, windows-latest, macos-latest]
        python-version: ['3.8', '3.9', '3.10', '3.11', '3.12']
    
    runs-on: ${{ matrix.os }}
    
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
      - name: Install dependencies
      - name: Run tests
      - name: Upload coverage
```

### Multiple Workflow Files

```
.github/workflows/
├── ci.yml                    # General CI testing
├── build-binaries.yml        # Build executables
└── publish-to-pypi.yml       # Publish to PyPI
```

**Why separate workflows?**
- Different triggers (push vs tag)
- Different purposes
- Easier to maintain
- Independent execution

### Workflow Best Practices

```yaml
# ✅ Use specific versions
- uses: actions/checkout@v4          # Version specified
- uses: actions/upload-artifact@v4   # Updated to v4

# ❌ Avoid
- uses: actions/checkout@latest      # Unstable

# ✅ Matrix builds for cross-platform
strategy:
  matrix:
    os: [ubuntu-latest, windows-latest, macos-latest]
    python-version: ['3.8', '3.11', '3.12']

# ✅ Conditional steps
- name: Windows-specific
  if: runner.os == 'Windows'
  run: choco install something

# ✅ Proper permissions
permissions:
  contents: write              # For creating releases
```

---

## Testing Strategy

### Test Organization

```
tests/
├── test_core.py           # Unit tests for core logic
├── test_cli.py            # CLI interface tests
├── test_gui.py            # GUI tests (if applicable)
├── test_integration.py    # End-to-end tests
└── fixtures/              # Test data
    └── samples/
```

### Test Patterns

```python
# test_extractor.py
import pytest
from pathlib import Path

class TestMusicExtractor:
    """Test music metadata extraction."""
    
    @pytest.fixture
    def extractor(self):
        """Provide extractor instance."""
        return MusicFileExtractor()
    
    @pytest.fixture
    def test_file(self, tmp_path):
        """Create temporary test file."""
        file_path = tmp_path / "test.mp3"
        file_path.write_bytes(b"test data")
        return file_path
    
    def test_extract_metadata(self, extractor, test_file):
        """Test metadata extraction from MP3."""
        # Arrange
        expected_title = "Test Song"
        
        # Act
        metadata = extractor.extract(test_file)
        
        # Assert
        assert metadata["title"] == expected_title
        assert metadata["artist"] is not None
    
    def test_invalid_file(self, extractor):
        """Test handling of invalid files."""
        with pytest.raises(FileNotFoundError):
            extractor.extract("nonexistent.mp3")
```

### Test Coverage Goals

- **Core logic**: 95%+ coverage
- **CLI**: 80%+ coverage (UI logic harder to test)
- **Integration**: Complete user workflows
- **Edge cases**: Empty inputs, special characters, large files

### Running Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=package_name --cov-report=html

# Specific test
pytest tests/test_core.py::TestClass::test_method

# Verbose
pytest -v

# Stop on first failure
pytest -x
```

---

## Release Management

### Version Numbering (SemVer)

```
MAJOR.MINOR.PATCH
  1  .  0  .  6

MAJOR: Breaking changes (2.0.0)
MINOR: New features, backward-compatible (1.1.0)
PATCH: Bug fixes (1.0.1)
```

### Version Update Checklist

```markdown
- [ ] Update version in setup.py
- [ ] Update version in pyproject.toml
- [ ] Update version in src/package/__init__.py
- [ ] Update CHANGELOG.md (if exists)
- [ ] Run all tests
- [ ] Build locally and test
- [ ] Create git tag
- [ ] Push tag to trigger workflows
```

### Version Update Locations

```python
# setup.py
setup(
    name="package-name",
    version="1.0.6",  # ← Update here
    ...
)

# pyproject.toml
[project]
version = "1.0.6"  # ← Update here

# src/package/__init__.py
__version__ = "1.0.6"  # ← Update here
```

### Git Tagging

```bash
# Create annotated tag
git tag -a v1.0.6 -m "Release version 1.0.6"

# Push tag (triggers workflows)
git push origin v1.0.6

# List tags
git tag -l

# Delete tag (if mistake)
git tag -d v1.0.6
git push origin :refs/tags/v1.0.6
```

---

## Package Distribution

### Multiple Distribution Methods

1. **PyPI** (Python Package Index)
   - Primary method for Python packages
   - `pip install package-name`
   - Automated via GitHub Actions

2. **Homebrew** (macOS/Linux)
   - Native package manager integration
   - `brew install package-name`
   - Requires separate tap repository

3. **Docker** (Containerized)
   - Cross-platform consistency
   - No installation required
   - Ideal for servers

4. **Binary Executables**
   - PyInstaller-based
   - No Python required
   - Per-platform builds

### PyPI Publication Workflow

```yaml
# .github/workflows/publish-to-pypi.yml
name: Publish to PyPI

on:
  push:
    tags:
      - 'v*.*.*'

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Build package
        run: python -m build
      - uses: actions/upload-artifact@v4
  
  publish:
    needs: build
    environment: github-actions
    steps:
      - uses: pypa/gh-action-pypi-publish@release/v1
        with:
          password: ${{ secrets.PYPI_API_TOKEN }}
```

### Homebrew Formula Pattern

```ruby
class PackageName < Formula
  include Language::Python::Virtualenv

  desc "Package description"
  homepage "https://github.com/user/repo"
  url "https://files.pythonhosted.org/packages/.../package-1.0.6.tar.gz"
  sha256 "calculated_sha256"
  license "MIT"

  depends_on "python@3.11"

  resource "dependency" do
    url "..."
    sha256 "..."
  end

  def install
    virtualenv_install_with_resources
  end

  test do
    assert_match version.to_s, shell_output("#{bin}/package-name --version")
  end
end
```

---

## Development Workflow

### Branch Strategy

```
main                    # Production-ready code
├── feature/xxx         # New features
├── bugfix/xxx          # Bug fixes
├── docs/xxx            # Documentation updates
└── release/1.0.6       # Release preparation
```

### Commit Message Format

```
<type>: <description>

[optional body]

[optional footer]
```

**Types:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `test:` Tests
- `refactor:` Code refactoring
- `style:` Code style (formatting)
- `chore:` Maintenance

**Examples:**
```
feat: add duplicate detection with multiple strategies

fix: handle unicode characters in filenames on Windows

docs: add comprehensive troubleshooting guide

test: add integration tests for CSV export

chore: update GitHub Actions to v4
```

### Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation
- [ ] Breaking change

## Checklist
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] All tests passing
- [ ] Code follows style guide

## Testing
How were these changes tested?
```

---

## Code Style & Quality

### Python Style Guide

- **Line length**: 100 characters (not 80)
- **Quotes**: Double quotes for strings
- **Imports**: Grouped and sorted (isort)
- **Formatting**: Black formatter
- **Type hints**: Encouraged but not required

### Configuration Files

```ini
# mypy.ini
[mypy]
python_version = 3.8
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = false
```

```toml
# pyproject.toml
[tool.black]
line-length = 100
target-version = ['py38', 'py39', 'py310', 'py311', 'py312']

[tool.isort]
profile = "black"
line_length = 100
```

### Quality Checks

```bash
# Format code
black src tests

# Sort imports
isort src tests

# Linting
flake8 src tests --max-line-length=100

# Type checking
mypy src

# All checks
black . && isort . && flake8 . && mypy src && pytest
```

---

## Environment-Specific Guidelines

### Docker Best Practices

```dockerfile
# Multi-stage build for smaller images
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY . /app
WORKDIR /app
ENTRYPOINT ["python", "-m", "package_name.cli"]
```

### Windows Compatibility

```python
# ✅ Use pathlib for cross-platform paths
from pathlib import Path
file_path = Path("folder") / "file.txt"

# ❌ Avoid string concatenation
file_path = "folder\\file.txt"  # Windows only

# ✅ Handle line endings
with open(file, "w", newline="") as f:  # Consistent line endings
    writer = csv.writer(f)
```

### Unicode Handling

```python
# ✅ Explicit encoding
with open(file, "r", encoding="utf-8") as f:
    content = f.read()

# ✅ Binary I/O when needed
with open(file, "rb") as f:
    metadata = mutagen.File(f)
```

---

## Example: Complete Feature Implementation

### Scenario: Adding PDF Export

```
1. Create feature branch
   git checkout -b feature/pdf-export

2. Implement core logic
   src/package/pdf_exporter.py

3. Add tests
   tests/test_pdf_exporter.py

4. Update CLI
   src/package/cli.py (add --format pdf option)

5. Update documentation
   - README.md (add to features)
   - docs/USAGE_EXAMPLES.md (add examples)

6. Run quality checks
   black . && isort . && flake8 . && pytest

7. Commit
   git commit -m "feat: add PDF export functionality"

8. Create PR
   - Include description
   - Link related issues
   - Request review

9. Merge after approval
10. Tag release if needed
```

---

## Summary: Key Takeaways

### Structure
- `src/` for source code
- Separate `tests/` directory
- Multiple specialized documentation files
- Clear separation of concerns

### Workflows
- Multi-platform CI/CD
- Automated testing and building
- Tag-based releases
- Multiple distribution channels

### Quality
- 90%+ test coverage goal
- Automated code formatting
- Type hints where beneficial
- Comprehensive documentation

### Distribution
- PyPI as primary
- Homebrew for macOS/Linux
- Docker for containerization
- Binaries for non-technical users

### Development
- SemVer versioning
- Conventional commits
- Feature branches
- Detailed PR templates

---

This structure ensures:
✅ Professional appearance
✅ Easy maintenance
✅ Cross-platform compatibility  
✅ Multiple user types supported
✅ Automated quality assurance
✅ Clear contribution path
✅ Scalable architecture

Use this as a blueprint for any new Python project!
