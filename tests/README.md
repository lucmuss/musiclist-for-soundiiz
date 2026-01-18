# Test-Dokumentation

Diese Test-Suite stellt sicher, dass MusicList for Soundiiz korrekt funktioniert.

## Test-Struktur

```
tests/
├── __init__.py
├── README.md                    # Diese Datei
├── test_extractor.py           # Unit-Tests für Metadaten-Extraktion
├── test_exporter.py            # Unit-Tests für Export-Funktionen
├── test_integration.py         # Integration-Tests mit echten Audiodateien
└── fixtures/                   # Test-Fixtures
    └── music/                  # Verschachtelte Verzeichnisstruktur
        ├── Rock/
        │   ├── test_file.mp3
        │   └── test_file.flac
        ├── Pop/
        │   └── test_file.aac
        └── Electronic/
            ├── test_file.wma
            └── Techno/
                └── test_file.ogg
```

## Test-Kategorien

### 1. Unit-Tests (test_extractor.py)

**Testet:** Metadaten-Extraktion und Datei-Scanning

- ✅ Unterstützung aller Audio-Formate (AAC, AU, FLAC, MP3, OGG, M4A, WAV, WMA)
- ✅ Rekursives/nicht-rekursives Scannen
- ✅ Dateinamen-Parsing ("Artist - Title" Format)
- ✅ Fehlerbehandlung bei ungültigen Dateien
- ✅ Case-insensitive Dateierweiterungen
- ✅ Filterung nach Extensions

**46 Tests** - Deckt alle Edge-Cases ab

### 2. Unit-Tests (test_exporter.py)

**Testet:** Export in verschiedene Formate

- ✅ CSV-Export (Soundiiz-kompatibel)
  - Mit Sonderzeichen (Kommas, Anführungszeichen)
  - Automatische Aufteilung bei großen Playlists
  - Korrekte Header-Formatierung
- ✅ JSON-Export (Pretty & Compact)
- ✅ M3U-Export (Extended & Simple)
- ✅ TXT-Export
- ✅ Unicode-Support

**24 Tests** - Validiert alle Export-Formate

### 3. Integration-Tests (test_integration.py)

**Testet:** End-to-End Workflows mit echten Audiodateien

#### TestRealAudioFiles (5 Tests)
Validiert Metadaten-Extraktion aus echten Audio-Dateien:

```python
# Beispiel: MP3 Metadaten-Test
metadata = extractor.extract_metadata("test_file.mp3")
assert metadata["title"] == "Loneliness"
assert metadata["artist"] == "Tomcraft"
assert metadata["album"] == "Loneliness"
```

**Getestete Formate:**
- MP3 (Rock/test_file.mp3)
- FLAC (Rock/test_file.flac)
- AAC (Pop/test_file.aac)
- OGG (Electronic/Techno/test_file.ogg)
- WMA (Electronic/test_file.wma)

#### TestNestedDirectoryStructure (5 Tests)
Testet verschachtelte Verzeichnisstrukturen:

- ✅ Rekursives Scannen findet alle Dateien in Unterordnern
- ✅ Nicht-rekursives Scannen nur Top-Level
- ✅ Metadaten-Extraktion aus verschachtelten Strukturen
- ✅ Filterung nach Extension in verschachtelten Ordnern
- ✅ Multiple Formate im selben Verzeichnis

#### TestEndToEndWorkflow (3 Tests)
Vollständige Workflows:

1. **CSV-Export-Workflow**
   - Scannen → Extrahieren → CSV exportieren
   - Validierung des Soundiiz-Formats
   
2. **JSON-Export-Workflow**
   - Scannen → Extrahieren → JSON exportieren
   - JSON-Struktur validieren

3. **Metadaten-Konsistenz**
   - Gleicher Song in verschiedenen Formaten
   - Konsistente Metadaten über Formate hinweg

## Test-Fixtures

### Verzeichnisstruktur

Die Test-Fixtures simulieren eine echte Musikbibliothek:

```
fixtures/music/
├── Rock/              # Genre-Ordner mit mehreren Formaten
│   ├── test_file.mp3  # Loneliness - Tomcraft
│   └── test_file.flac # Loneliness - Tomcraft
├── Pop/               # Anderes Genre
│   └── test_file.aac  # Loneliness - Tomcraft
└── Electronic/        # Verschachteltes Genre
    ├── test_file.wma
    └── Techno/        # Sub-Genre
        └── test_file.ogg # Loneliness - Tomcraft
```

### Echte Audiodateien

Alle Test-Dateien sind **echte Audiodateien** mit eingebetteten Metadaten:

| Datei | Format | Titel | Artist | Album |
|-------|--------|-------|--------|-------|
| test_file.mp3 | MP3 | Loneliness | Tomcraft | Loneliness |
| test_file.flac | FLAC | Loneliness | Tomcraft | Loneliness |
| test_file.aac | AAC | Loneliness | Tomcraft | Loneliness |
| test_file.ogg | OGG Vorbis | Loneliness | Tomcraft | Loneliness |
| test_file.wma | WMA | test_file | Unknown Artist | Unknown Album |

## Tests ausführen

### Alle Tests

```bash
pytest
```

### Mit Coverage

```bash
pytest --cov=musiclist_for_soundiiz --cov-report=html
```

### Nur Unit-Tests

```bash
pytest tests/test_extractor.py tests/test_exporter.py
```

### Nur Integration-Tests

```bash
pytest tests/test_integration.py
```

### Einzelne Test-Klasse

```bash
pytest tests/test_integration.py::TestRealAudioFiles
```

### Einzelner Test

```bash
pytest tests/test_integration.py::TestRealAudioFiles::test_extract_mp3_metadata -v
```

### Mit Verbose-Output

```bash
pytest -v
```

## Test-Coverage

Aktuell: **77% Code Coverage**

- `__init__.py`: 100%
- `exporter.py`: 99%
- `extractor.py`: 95%
- `cli.py`: 18% (CLI wird hauptsächlich manuell getestet)

## Neue Tests hinzufügen

### Unit-Test Beispiel

```python
def test_new_feature(self):
    """Test description."""
    # Arrange
    extractor = MusicFileExtractor()
    
    # Act
    result = extractor.some_method()
    
    # Assert
    assert result == expected_value
```

### Integration-Test mit Fixtures

```python
def test_with_real_file(self, fixtures_dir):
    """Test with real audio file."""
    audio_file = fixtures_dir / "Rock" / "test_file.mp3"
    
    if not audio_file.exists():
        pytest.skip(f"File not found: {audio_file}")
    
    extractor = MusicFileExtractor()
    metadata = extractor.extract_metadata(audio_file)
    
    assert metadata["title"] == "Loneliness"
```

## Continuous Integration

Tests werden automatisch bei jedem Push/Pull Request ausgeführt:

- **GitHub Actions** (`.github/workflows/ci.yml`)
- **Multi-Platform**: Linux, Windows, macOS
- **Multi-Python**: 3.8, 3.9, 3.10, 3.11, 3.12

## Best Practices

1. **Jeden Test isoliert halten** - Keine Abhängigkeiten zwischen Tests
2. **Fixtures verwenden** - Für wiederverwendbare Test-Daten
3. **Klare Assertions** - Was wird getestet und warum
4. **Edge Cases testen** - Leere Verzeichnisse, fehlerhafte Dateien, etc.
5. **Reale Daten verwenden** - Integration-Tests mit echten Audiodateien

## Fehlersuche

### Test schlägt fehl

```bash
# Einzelnen Test mit Verbose-Output ausführen
pytest tests/test_integration.py::test_name -vv

# Mit Debugger
pytest --pdb tests/test_integration.py::test_name
```

### Fixtures nicht gefunden

```bash
# Überprüfe, ob Fixtures existieren
ls -la tests/fixtures/music/Rock/
```

### Import-Fehler

```bash
# Stelle sicher, dass Paket installiert ist
pip install -e .
```

## Statistiken

- **Gesamt**: 59 Tests
- **Unit-Tests**: 46
- **Integration-Tests**: 13
- **Test-Runtime**: ~0.3s
- **Coverage**: 77%
- **Status**: ✅ Alle Tests bestehen
