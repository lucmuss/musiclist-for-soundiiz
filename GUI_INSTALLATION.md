# GUI Installation Guide

## Problem: ModuleNotFoundError: No module named 'tkinter'

Tkinter ist normalerweise nicht in virtuellen Python-Umgebungen enthalten. Hier ist die Lösung:

---

## ✅ Lösung: Tkinter System-Wide installieren

### Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install python3-tk
```

### Fedora/RHEL:
```bash
sudo dnf install python3-tkinter
```

### macOS:
```bash
# Tkinter ist normalerweise mit Python vorinstalliert
# Falls nicht:
brew install python-tk
```

### Windows:
Tkinter ist standardmäßig mit Python installiert. Keine zusätzlichen Schritte nötig.

---

## 🧪 Testen ob Tkinter installiert ist:

```bash
python3 -m tkinter
```

✅ **Erfolgreich**: Ein kleines Testfenster sollte erscheinen  
❌ **Fehler**: Tkinter ist nicht installiert

---

## 🚀 Nach der Installation:

```bash
# Wechsel in dein Projektverzeichnis
cd /home/skymuss/projects/musiclist-for-soundiiz

# Aktiviere virtuelle Umgebung
source venv/bin/activate

# Starte die GUI
musiclist-for-soundiiz-gui
```

---

## 🔧 Alternative: GUI ohne Installation starten

Falls du Tkinter nicht installieren kannst, starte die GUI direkt aus dem System-Python:

```bash
# OHNE virtuelle Umgebung
cd /home/skymuss/projects/musiclist-for-soundiiz

# Installiere nur Mutagen system-wide
pip3 install mutagen --user

# Starte GUI direkt
python3 src/musiclist_for_soundiiz/gui.py
```

**Hinweis**: Dies funktioniert, weil Tkinter system-wide verfügbar ist, auch wenn es nicht in der venv ist.

---

## 📝 Warum passiert das?

- Tkinter ist eine C-Extension
- Virtual Environments kopieren es nicht automatisch
- Muss system-wide installiert werden
- Aber: Funktioniert dann in allen venvs

---

## ✅ Schnelle Schritt-für-Schritt-Lösung

```bash
# 1. Tkinter installieren (erfordert sudo/Admin)
sudo apt-get install python3-tk

# 2. Testen
python3 -m tkinter

# 3. GUI starten
cd /home/skymuss/projects/musiclist-for-soundiiz
source venv/bin/activate
musiclist-for-soundiiz-gui
```

---

## 🆘 Immer noch Probleme?

### Check 1: Python Version
```bash
python3 --version
# GUI benötigt Python 3.8+
```

### Check 2: Tkinter Version
```bash
python3 -c "import tkinter; print(tkinter.TkVersion)"
# Sollte 8.6 oder höher sein
```

### Check 3: Pfade
```bash
which python3
which musiclist-for-soundiiz-gui
```

---

## 💡 Tipp: In Dokumentation aufnehmen

Füge dies zu deinem README hinzu, unter "Prerequisites":

```markdown
## Prerequisites

- Python 3.8 or higher
- Tkinter (for GUI):
  - Ubuntu/Debian: `sudo apt-get install python3-tk`
  - macOS: Pre-installed with Python
  - Windows: Pre-installed with Python
```

---

**Problem gelöst? Starte die GUI und viel Spaß! 🎉**
