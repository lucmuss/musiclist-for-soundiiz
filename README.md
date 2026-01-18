# MusicList for Soundiiz 🎵

[![CI](https://github.com/lucmuss/musiclist-for-soundiiz/workflows/CI/badge.svg)](https://github.com/lucmuss/musiclist-for-soundiiz/actions)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Professionelles Kommandozeilen-Tool zum Extrahieren von Musikdatei-Metadaten für den Import in Soundiiz.

## ✨ Features

- **🎵 Multi-Format-Unterstützung** - AAC, AU, FLAC, MP3, OGG, M4A, WAV, WMA
- **📊 Mehrere Export-Formate** - CSV (Soundiiz), JSON, M3U, TXT
- **🔍 Intelligente Metadaten-Extraktion** - Liest Tags und parst Dateinamen (Format: "Artist - Title")
- **📁 Rekursives Scannen** - Durchsucht automatisch alle Unterverzeichnisse
- **🔄 Automatische CSV-Aufteilung** - Teilt große Playlists in mehrere Dateien (konfigurierbar)
- **🛡️ Robuste Fehlerbehandlung** - Überspringt problematische Dateien und setzt den Prozess fort
- **✅ Production-Ready** - Vollständig getestet mit umfangreicher Test-Suite
- **🌐 Unicode-Support** - Korrekte Behandlung von Umlauten und Sonderzeichen
- **📝 Detailliertes Logging** - Verbose-Modus für Debugging

## 📋 Inhaltsverzeichnis

- [Installation](#installation)
- [Schnellstart](#schnellstart)
- [Verwendungsbeispiele](#verwendungsbeispiele)
- [Konfiguration](#konfiguration)
- [Export-Formate](#export-formate)
- [Soundiiz Import](#soundiiz-import)
- [Entwicklung](#entwicklung)
- [Tests](#tests)
- [Beitragen](#beitragen)
- [Lizenz](#lizenz)

## 🚀 Installation

### Voraussetzungen

- Python 3.8 oder höher

### Installation

```bash
# Repository klonen
git clone https://github.com/lucmuss/musiclist-for-soundiiz.git
cd musiclist-for-soundiiz

# Virtuelle Umgebung erstellen (empfohlen)
python -m venv venv
source venv/bin/activate  # Unter Windows: venv\Scripts\activate

# Paket installieren
pip install -e .

# Oder mit Entwicklungsabhängigkeiten
pip install -e ".[dev]"
```

## ⚡ Schnellstart

```bash
# Musikdateien scannen und als CSV exportieren
musiclist-for-soundiiz -i /pfad/zu/musik -o output.csv

# Ergebnis: output.csv (bereit für Soundiiz Import)
```

## 📚 Verwendungsbeispiele

### 🎯 Basis-Verwendung

```bash
# Verzeichnis scannen und CSV erstellen
musiclist-for-soundiiz -i /music/library -o soundiiz.csv
```

### 📝 Verschiedene Export-Formate

```bash
# CSV-Export (Standard, für Soundiiz)
musiclist-for-soundiiz -i /music -o playlist.csv -f csv

# JSON-Export (mit allen Metadaten)
musiclist-for-soundiiz -i /music -o playlist.json -f json

# M3U-Playlist erstellen
musiclist-for-soundiiz -i /music -o playlist.m3u -f m3u

# Einfache Textliste (Titel - Artist)
musiclist-for-soundiiz -i /music -o playlist.txt -f txt
```

### 🎨 Nur bestimmte Dateiformate

```bash
# Nur MP3 und FLAC Dateien
musiclist-for-soundiiz -i /music -e .mp3 .flac -o output.csv

# Nur OGG Dateien
musiclist-for-soundiiz -i /music -e .ogg -o ogg_files.csv
```

### 📁 Nicht-rekursives Scannen

```bash
# Nur aktuelles Verzeichnis (keine Unterordner)
musiclist-for-soundiiz -i /music --no-recursive -o output.csv
```

### 🔧 CSV-Optionen anpassen

```bash
# Maximale Anzahl Songs pro CSV-Datei
musiclist-for-soundiiz -i /music -o output.csv --max-songs-per-file 200

# Bei mehr als 200 Songs werden mehrere Dateien erstellt:
# output_1.csv, output_2.csv, output_3.csv, ...
```

### 🔍 Verbose-Modus (Debugging)

```bash
# Detaillierte Ausgabe für Debugging
musiclist-for-soundiiz -i /music -o output.csv -v

# Oder komplett still (nur Fehler)
musiclist-for-soundiiz -i /music -o output.csv -q
```

## ⚙️ Konfiguration

### Kommandozeilen-Optionen

| Option | Beschreibung | Standard |
|--------|--------------|----------|
| `-i, --input` | Pfad zum Musik-Verzeichnis | **Erforderlich** |
| `-o, --output` | Pfad zur Ausgabedatei | `output.csv` |
| `-f, --format` | Export-Format (csv/json/m3u/txt) | `csv` |
| `-e, --extensions` | Dateierweiterungen zum Filtern | Alle unterstützten |
| `--no-recursive` | Keine Unterverzeichnisse scannen | `false` |
| `--max-songs-per-file` | Max. Songs pro CSV-Datei | `500` |
| `--no-pretty-json` | Kompaktes JSON (ohne Einrückung) | `false` |
| `-v, --verbose` | Verbose-Logging aktivieren | `false` |
| `-q, --quiet` | Nur Fehler ausgeben | `false` |
| `--version` | Version anzeigen | - |

## 📄 Export-Formate

### CSV (Soundiiz-kompatibel)

```csv
title,artist,album,isrc,
Song Title,Artist Name,Album Name,,
Another Song,"Artist, with comma",Album 2,,
```

**Hinweis:** Das abschließende Komma ist Teil der Soundiiz-Spezifikation.

### JSON

```json
{
  "total_songs": 2,
  "songs": [
    {
      "title": "Song Title",
      "artist": "Artist Name",
      "album": "Album Name",
      "isrc": "",
      "genre": "Rock",
      "year": "2020",
      "duration": "180",
      "file_path": "/path/to/song.mp3",
      "filename": "song.mp3"
    }
  ]
}
```

### M3U (Playlist)

```
#EXTM3U
#EXTINF:180,Artist Name - Song Title
/path/to/song.mp3
```

### TXT (Einfache Liste)

```
Song Title - Artist Name
Another Song - Another Artist
```

## 🎵 Soundiiz Import

### Schritt-für-Schritt Anleitung

1. **CSV-Datei erstellen:**
   ```bash
   musiclist-for-soundiiz -i /pfad/zu/musik -o meine_musik.csv
   ```

2. **Zu Soundiiz gehen:**
   - Öffne [soundiiz.com](https://soundiiz.com)
   - Melde dich an

3. **Import starten:**
   - Klicke auf "Import"
   - Wähle "CSV File"
   - Lade deine `meine_musik.csv` hoch

4. **Zu Streaming-Dienst exportieren:**
   - Wähle Ziel-Plattform (Spotify, Apple Music, etc.)
   - Bestätige den Export

### Unterstützte Audio-Formate

✅ **AAC** (.aac) - Advanced Audio Coding  
✅ **AU** (.au) - AU Audio File  
✅ **FLAC** (.flac) - Free Lossless Audio Codec  
✅ **MP3** (.mp3) - MPEG Audio Layer III  
✅ **OGG** (.ogg) - OGG Vorbis  
✅ **M4A** (.m4a) - MPEG-4 Audio  
✅ **WAV** (.wav) - Waveform Audio File  
✅ **WMA** (.wma) - Windows Media Audio  

## 💻 Entwicklung

### Entwicklungsumgebung einrichten

```bash
# Repository klonen
git clone https://github.com/lucmuss/musiclist-for-soundiiz.git
cd musiclist-for-soundiiz

# Virtuelle Umgebung erstellen
python -m venv venv
source venv/bin/activate

# Development-Abhängigkeiten installieren
pip install -e ".[dev]"
```

### Code-Qualität

```bash
# Code formatieren
black src tests

# Imports sortieren
isort src tests

# Linting
flake8 src tests --max-line-length=100

# Type-Checking
mypy src
```

## 🧪 Tests

### Tests ausführen

```bash
# Alle Tests ausführen
pytest

# Mit Coverage-Report
pytest --cov=musiclist_for_soundiiz --cov-report=html

# Spezifische Test-Datei
pytest tests/test_extractor.py

# Verbose-Modus
pytest -v
```

### Test-Coverage

Das Projekt hat eine umfassende Test-Suite:

- ✅ Unit-Tests für alle Formate (AAC, AU, FLAC, MP3, OGG)
- ✅ Tests für alle Export-Formate (CSV, JSON, M3U, TXT)
- ✅ Tests für Fehlerbehandlung
- ✅ Tests für Edge-Cases (Sonderzeichen, Unicode, etc.)
- ✅ Tests für rekursives/nicht-rekursives Scannen

## 📊 Projekt-Struktur

```
musiclist-for-soundiiz/
├── src/
│   └── musiclist_for_soundiiz/
│       ├── __init__.py
│       ├── cli.py           # Kommandozeilen-Interface
│       ├── extractor.py     # Metadaten-Extraktion
│       └── exporter.py      # Export-Funktionalität
├── tests/
│   ├── __init__.py
│   ├── test_extractor.py    # Extractor-Tests
│   └── test_exporter.py     # Exporter-Tests
├── .github/
│   └── workflows/
│       └── ci.yml           # GitHub Actions CI/CD
├── setup.py                 # Paket-Konfiguration
├── requirements.txt         # Dependencies
├── requirements-dev.txt     # Dev-Dependencies
├── .gitignore
├── LICENSE
├── CONTRIBUTING.md
└── README.md
```

## 🤝 Beitragen

Beiträge sind willkommen! Siehe [CONTRIBUTING.md](CONTRIBUTING.md) für Details.

### Schnelle Schritte

1. Fork das Repository
2. Erstelle einen Feature-Branch (`git checkout -b feature/amazing-feature`)
3. Mache deine Änderungen
4. Füge Tests hinzu
5. Führe Tests aus (`pytest`)
6. Commit (`git commit -m 'feat: add amazing feature'`)
7. Push (`git push origin feature/amazing-feature`)
8. Erstelle einen Pull Request

## 📝 Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert - siehe [LICENSE](LICENSE) für Details.

## 🙏 Danksagungen

Erstellt mit:
- [Mutagen](https://github.com/quodlibet/mutagen) - Python Audio Metadata Library
- [pytest](https://pytest.org/) - Testing Framework

## 📞 Support

- **Issues:** [GitHub Issues](https://github.com/lucmuss/musiclist-for-soundiiz/issues)
- **Discussions:** [GitHub Discussions](https://github.com/lucmuss/musiclist-for-soundiiz/discussions)
- **Dokumentation:** [README](https://github.com/lucmuss/musiclist-for-soundiiz#readme)

## 🗺️ Roadmap

- [ ] GUI-Interface (tkinter/PyQt)
- [ ] Automatische Duplikat-Erkennung
- [ ] Batch-Verarbeitung mehrerer Verzeichnisse
- [ ] Spotify/Apple Music Direktintegration
- [ ] Docker Container
- [ ] Web-Interface

## 💡 Beispiele

### Große Musikbibliothek verarbeiten

```bash
# 10.000+ Songs scannen und in mehrere CSV-Dateien aufteilen
musiclist-for-soundiiz -i /große/bibliothek -o playlist.csv --max-songs-per-file 500
# Erstellt: playlist_1.csv, playlist_2.csv, playlist_3.csv, ...
```

### Nur verlustfreie Formate

```bash
# Nur FLAC und WAV
musiclist-for-soundiiz -i /music -e .flac .wav -o lossless.csv
```

### Komplett-Export (alle Formate)

```bash
# CSV für Soundiiz
musiclist-for-soundiiz -i /music -o soundiiz.csv -f csv

# JSON für Backup/Analyse
musiclist-for-soundiiz -i /music -o backup.json -f json

# M3U für Media Player
musiclist-for-soundiiz -i /music -o playlist.m3u -f m3u
```

---

**Entwickelt mit ❤️ für die Musik-Community**
