# Beitragen zu MusicList for Soundiiz

Vielen Dank für dein Interesse, zu diesem Projekt beizutragen! 🎵

## 📋 Inhaltsverzeichnis

- [Code of Conduct](#code-of-conduct)
- [Wie kann ich beitragen?](#wie-kann-ich-beitragen)
- [Entwicklungsumgebung einrichten](#entwicklungsumgebung-einrichten)
- [Entwicklungsprozess](#entwicklungsprozess)
- [Tests schreiben](#tests-schreiben)
- [Code-Stil](#code-stil)
- [Pull Request Prozess](#pull-request-prozess)
- [Issue Guidelines](#issue-guidelines)

## Code of Conduct

Dieses Projekt folgt einem Code of Conduct. Durch deine Teilnahme verpflichtest du dich, diesen einzuhalten. Bitte melde unangemessenes Verhalten.

## Wie kann ich beitragen?

### 🐛 Bugs melden

Wenn du einen Bug findest:

1. Prüfe, ob der Bug bereits in den [Issues](https://github.com/lucmuss/musiclist-for-soundiiz/issues) gemeldet wurde
2. Falls nicht, erstelle ein neues Issue mit:
   - Beschreibendem Titel
   - Schritten zur Reproduktion
   - Erwartetes vs. tatsächliches Verhalten
   - Deine Umgebung (OS, Python-Version)
   - Relevante Log-Ausgaben

### 💡 Features vorschlagen

Feature-Vorschläge sind willkommen! Bitte:

1. Prüfe existierende Feature Requests
2. Erstelle ein Issue mit:
   - Klarer Beschreibung des Features
   - Anwendungsfällen
   - Möglicher Implementierung

### 🔧 Code beitragen

1. Fork das Repository
2. Erstelle einen Feature-Branch
3. Implementiere deine Änderungen
4. Schreibe Tests
5. Stelle sicher, dass alle Tests bestehen
6. Erstelle einen Pull Request

## Entwicklungsumgebung einrichten

### Voraussetzungen

- Python 3.8+
- Git

### Setup

```bash
# Repository forken und klonen
git clone https://github.com/DEIN-USERNAME/musiclist-for-soundiiz.git
cd musiclist-for-soundiiz

# Virtuelle Umgebung erstellen
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Development-Abhängigkeiten installieren
pip install -e ".[dev]"
```

## Entwicklungsprozess

### Branch-Namenskonventionen

- `feature/` - Neue Features (z.B. `feature/add-spotify-export`)
- `bugfix/` - Bugfixes (z.B. `bugfix/fix-unicode-issue`)
- `docs/` - Dokumentations-Updates (z.B. `docs/improve-readme`)
- `test/` - Test-Verbesserungen (z.B. `test/add-integration-tests`)

### Commit-Nachrichten

Wir folgen [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>: <description>

[optional body]

[optional footer]
```

**Types:**
- `feat:` - Neues Feature
- `fix:` - Bugfix
- `docs:` - Dokumentation
- `test:` - Tests
- `refactor:` - Code-Refactoring
- `style:` - Code-Stil (Formatierung)
- `chore:` - Wartungsarbeiten

**Beispiele:**
```bash
feat: add support for Spotify playlists
fix: handle unicode characters in filenames
docs: update installation instructions
test: add tests for OGG format
```

## Tests schreiben

### Test-Struktur

```python
def test_descriptive_name(self):
    """Clear description of what is being tested."""
    # Arrange
    extractor = MusicFileExtractor()
    
    # Act
    result = extractor.find_music_files(test_dir)
    
    # Assert
    assert len(result) == expected_count
```

### Tests ausführen

```bash
# Alle Tests
pytest

# Mit Coverage
pytest --cov=musiclist_for_soundiiz --cov-report=html

# Einzelne Datei
pytest tests/test_extractor.py

# Einzelner Test
pytest tests/test_extractor.py::TestMusicFileExtractor::test_find_music_files_mp3
```

### Test-Coverage

- Neue Features müssen mit Tests abgedeckt sein
- Ziel: >90% Code Coverage
- Edge Cases und Fehlerbehandlung testen

## Code-Stil

### Python Style Guide

Wir folgen [PEP 8](https://www.python.org/dev/peps/pep-0008/) mit einigen Anpassungen:

- Maximale Zeilenlänge: 100 Zeichen
- Code-Formatierung mit `black`
- Import-Sortierung mit `isort`
- Type Hints verwenden

### Code-Qualitäts-Tools

```bash
# Code formatieren
black src tests

# Imports sortieren
isort src tests

# Linting
flake8 src tests --max-line-length=100

# Type Checking
mypy src
```

### Pre-Commit

Empfohlen: Automatische Code-Qualitätsprüfung vor Commits:

```bash
pip install pre-commit
pre-commit install
```

## Pull Request Prozess

### Vor dem Pull Request

✅ **Checkliste:**

- [ ] Code folgt dem Projekt-Stil
- [ ] Alle Tests bestehen (`pytest`)
- [ ] Neue Tests für neue Features/Fixes hinzugefügt
- [ ] Dokumentation aktualisiert (falls nötig)
- [ ] Code-Qualitäts-Tools ausgeführt
- [ ] Branch ist aktuell mit main
- [ ] Commit-Nachrichten folgen Konventionen

### Pull Request erstellen

1. **Titel:** Klarer, beschreibender Titel
   ```
   feat: add support for WMA format
   ```

2. **Beschreibung:**
   ```markdown
   ## Änderungen
   - Added WMA file extension support
   - Added tests for WMA format
   - Updated documentation
   
   ## Motivation
   Users requested WMA support for Windows Media files
   
   ## Tests
   - Added unit tests for WMA file detection
   - All existing tests still pass
   
   Closes #42
   ```

3. **Review-Prozess:**
   - Mindestens eine Approval erforderlich
   - CI-Tests müssen bestehen
   - Code-Review-Kommentare beheben

## Issue Guidelines

### Bug Reports

```markdown
**Beschreibung:**
Kurze Zusammenfassung des Problems

**Schritte zur Reproduktion:**
1. Führe `musiclist-for-soundiiz -i /path` aus
2. ...

**Erwartetes Verhalten:**
Was sollte passieren

**Tatsächliches Verhalten:**
Was passiert tatsächlich

**Umgebung:**
- OS: Ubuntu 22.04
- Python: 3.10.5
- Version: 1.0.0

**Logs:**
```
ERROR-Ausgabe hier
```
```

### Feature Requests

```markdown
**Feature-Beschreibung:**
Klare Beschreibung des gewünschten Features

**Anwendungsfall:**
Warum ist dieses Feature nützlich?

**Vorgeschlagene Implementierung:**
(Optional) Ideen zur Umsetzung

**Alternativen:**
Andere Lösungen, die du in Betracht gezogen hast
```

## Entwicklungs-Tipps

### Debugging

```bash
# Verbose-Modus für detaillierte Logs
musiclist-for-soundiiz -i /test -o output.csv -v

# Python-Debugger verwenden
python -m pdb -m musiclist_for_soundiiz.cli -i /test -o output.csv
```

### Test-Daten erstellen

```python
# In Tests: Temporäre Testdateien erstellen
def test_example(tmp_path):
    test_file = tmp_path / "test.mp3"
    test_file.touch()
    # ...
```

### Nützliche Ressourcen

- [Python Testing Best Practices](https://docs.python-guide.org/writing/tests/)
- [Mutagen Documentation](https://mutagen.readthedocs.io/)
- [pytest Documentation](https://docs.pytest.org/)

## Fragen?

Bei Fragen:

- Erstelle ein [Discussion](https://github.com/lucmuss/musiclist-for-soundiiz/discussions)
- Frage in einem existierenden Issue
- Kontaktiere die Maintainer

## Lizenz

Durch deine Beiträge stimmst du zu, dass deine Arbeit unter der MIT-Lizenz lizenziert wird.

---

**Vielen Dank für deine Beiträge! 🙏**
