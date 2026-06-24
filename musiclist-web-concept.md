# Konzept: MusicList for Soundiiz - Django Web Application

## Ziel
Umwandlung des bestehenden CLI/GUI-Tools "MusicList for Soundiiz" in eine vollständige Django-Web-Anwendung mit dem gleichen Tech-Stack wie RedFlag Analyzer.

## Ausgangslage

### Bestehendes CLI-Tool (musiclist-for-soundiiz)
- **Funktion**: Extrahiert Metadaten aus Musikdateien
- **Formate**: AAC, AU, FLAC, MP3, OGG, M4A, WAV, WMA
- **Exporte**: CSV (Soundiiz), JSON, M3U, TXT
- **Features**: Recursive scanning, Duplicate detection, Batch processing
- **Tech**: Python 3.8+, uv, ruff, pytest

### Referenz-Projekt (RedFlag Analyzer)
- **Framework**: Django 5
- **Datenbank**: PostgreSQL
- **Struktur**: Modular unter `src/`
- **Deployment**: Docker + Railway
- **Testing**: pytest + Playwright E2E
- **Tools**: Justfile, uv, ruff, mypy

## Anforderungen

### 1. Django Projektstruktur (wie RedFlag Analyzer)
```
musiclist-web/
├── src/
│   ├── config/                 # Django settings
│   │   ├── settings/
│   │   │   ├── base.py
│   │   │   ├── development.py
│   │   │   └── production.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── apps/
│   │   ├── core/              # Basis-Funktionalität
│   │   ├── scanner/           # Musik-Scanning Logic
│   │   ├── playlists/         # Playlist Management
│   │   ├── exports/           # Export-Funktionen
│   │   └── api/               # REST API
│   ├── templates/
│   ├── static/
│   └── manage.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── docker/
├── nginx/
├── docs/
├── output/                    # Für Screenshots
├── Justfile
├── pyproject.toml
├── docker-compose.yml
└── railway.toml
```

### 2. Tech Stack (identisch zu RedFlag Analyzer)
- **Python**: 3.11+
- **Framework**: Django 5
- **Package Manager**: uv
- **Database**: PostgreSQL (SQLite für Tests)
- **Frontend**: Django Templates + HTMX (optional)
- **CSS**: Tailwind oder Bootstrap
- **Testing**: pytest, pytest-django, Playwright
- **Linting**: ruff, mypy
- **Task Runner**: just
- **Deployment**: Docker + Railway

### 3. Features (aus CLI übernehmen)

#### Core Features
- [ ] **Upload Interface**: Drag & Drop für Musik-Ordner
- [ ] **Scanning**: Rekursives Scannen von Verzeichnissen
- [ ] **Metadaten-Extraktion**: Titel, Künstler, Album, Genre, Jahr
- [ ] **Unterstützte Formate**: MP3, FLAC, M4A, OGG, WAV, WMA, AAC, AU

#### Playlist Management
- [ ] **Playlist-Erstellung**: Mehrere Playlists verwalten
- [ ] **Duplikat-Erkennung**: Identische Titel finden
- [ ] **Filter**: Nach Genre, Künstler, Album filtern
- [ ] **Suche**: Volltextsuche in Metadaten

#### Export-Funktionen
- [ ] **Soundiiz CSV**: Kompatibles Format für Soundiiz Import
- [ ] **JSON**: Vollständige Metadaten als JSON
- [ ] **M3U**: Playlist-Datei
- [ ] **TXT**: Einfache Text-Liste

#### Web-Specific Features
- [ ] **User Accounts**: Registrierung/Login
- [ ] **History**: Vergangene Scans/Playlists anzeigen
- [ ] **Download**: Export-Dateien herunterladen
- [ ] **Responsive Design**: Mobile-friendly

### 4. Datenmodelle

```python
# Scanner Models
class ScanSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    directory_path = models.CharField(max_length=1024)
    created_at = models.DateTimeField(auto_now_add=True)
    file_count = models.IntegerField(default=0)

class MusicFile(models.Model):
    scan_session = models.ForeignKey(ScanSession, on_delete=models.CASCADE)
    file_path = models.CharField(max_length=1024)
    title = models.CharField(max_length=500, blank=True)
    artist = models.CharField(max_length=500, blank=True)
    album = models.CharField(max_length=500, blank=True)
    genre = models.CharField(max_length=200, blank=True)
    year = models.IntegerField(null=True, blank=True)
    duration = models.FloatField(null=True)
    file_format = models.CharField(max_length=10)
    file_size = models.BigIntegerField()

# Playlist Models
class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class PlaylistItem(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    music_file = models.ForeignKey(MusicFile, on_delete=models.CASCADE)
    position = models.IntegerField()
    added_at = models.DateTimeField(auto_now_add=True)

# Export Models
class ExportJob(models.Model):
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    format = models.CharField(max_length=10)  # csv, json, m3u, txt
    status = models.CharField(max_length=20)  # pending, processing, completed, failed
    file_path = models.CharField(max_length=1024, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
```

### 5. Views/Pages

#### Public Pages
- [ ] **Landing Page**: Überblick über Features
- [ ] **About**: Projekt-Informationen

#### Authenticated Pages
- [ ] **Dashboard**: Übersicht der Scans und Playlists
- [ ] **Scan Upload**: Datei/Ordner-Upload Interface
- [ ] **Scan Results**: Anzeige der gescannten Dateien
- [ ] **Playlist List**: Alle Playlists des Users
- [ ] **Playlist Detail**: Einzelne Playlist mit Songs
- [ ] **Playlist Editor**: Songs hinzufügen/entfernen/reihenfolge
- [ ] **Export Page**: Export-Format auswählen und generieren
- [ ] **Download**: Export-Dateien herunterladen
- [ ] **History**: Vergangene Scans

#### Admin Pages
- [ ] **Django Admin**: Verwaltung aller Daten

### 6. API Endpoints (optional für SPA)
- [ ] `POST /api/scans/` - Neuen Scan starten
- [ ] `GET /api/scans/{id}/` - Scan-Details
- [ ] `GET /api/scans/{id}/files/` - Gescannte Dateien
- [ ] `GET /api/playlists/` - Playlists auflisten
- [ ] `POST /api/playlists/` - Neue Playlist erstellen
- [ ] `GET /api/playlists/{id}/` - Playlist-Details
- [ ] `POST /api/playlists/{id}/export/` - Playlist exportieren
- [ ] `GET /api/exports/{id}/download/` - Export herunterladen

### 7. Testing Requirements

#### Unit Tests
- [ ] Metadaten-Extraktion für jedes Format
- [ ] Duplikat-Erkennung
- [ ] Export-Format-Generierung
- [ ] Model Tests

#### Integration Tests
- [ ] Upload + Scanning Flow
- [ ] Playlist CRUD Operations
- [ ] Export Generation

#### E2E Tests (Playwright)
- [ ] Complete user journey: Upload → Scan → Create Playlist → Export
- [ ] UI interactions
- [ ] Responsive design tests

### 8. GUI-Analyse & Screenshots
- [ ] Screenshots aller Hauptseiten in `output/gui-screenshots/`
- [ ] GUI-Analyse für Usability
- [ ] Mobile/Responsive Screenshots

### 9. Justfile Commands (wie RedFlag Analyzer)
```just
# Setup
setup                      # Initial setup
bootstrap-env              # Bootstrap .env file
dev                        # Run development server

# Database
migrate                    # Run migrations
seed                       # Seed test data

# Quality
format                     # Format code with ruff
lint                       # Lint with ruff
typecheck                  # Type check with mypy
test                       # Run pytest
test-e2e                   # Run Playwright E2E tests
check                      # Run all quality checks

# Docker
docker-up                  # Start with Docker
docker-down                # Stop Docker

# Deployment
ci                         # Full CI pipeline
```

### 10. Deliverables
- [ ] Vollständige Django-Web-App
- [ ] Alle Features implementiert
- [ ] Tests (Unit, Integration, E2E)
- [ ] Screenshots in `output/gui-screenshots/`
- [ ] README.md mit Setup-Anleitung
- [ ] Docker-Setup funktionsfähig
- [ ] Alle Just-Befehle funktionieren
- [ ] Commit in Git

## Implementation Strategy
1. Django Projekt-Struktur aufsetzen (wie RedFlag Analyzer)
2. Models erstellen
3. Views und Templates
4. Upload/Scanning Logic (aus bestehendem CLI adaptieren)
5. Export-Funktionen
6. Testing
7. Screenshots + GUI-Analyse
8. Documentation
9. Final Check + Commit