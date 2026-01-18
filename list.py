# Scriptname: musiclist_for_soundiiz.py

import os
import logging

# Konfigurationsvariablen für musiclist_for_soundiiz.py
MUSICLISTFORSOUNDIIZ_DIRECTORY_TO_SCAN = "O:\\Kar"  # Pfad zum Verzeichnis mit Musikdateien
MUSICLISTFORSOUNDIIZ_OUTPUT_FILENAME_BASE = "ausgabe_"  # Basisname für die CSV-Ausgabedateien
MUSICLISTFORSOUNDIIZ_OUTPUT_FILE_EXTENSION = ".csv"  # Dateiendung für CSV-Dateien
MUSICLISTFORSOUNDIIZ_MAX_SONGS_PER_FILE = 200  # Maximale Anzahl Songs pro CSV-Datei
MUSICLISTFORSOUNDIIZ_LOGGING_ENABLED = True
MUSICLISTFORSOUNDIIZ_SUPPORTED_EXTENSIONS = [".mp3", ".flac", ".wav", ".m4a"]  # Unterstützte Musikdateien
MUSICLISTFORSOUNDIIZ_TXT_OUTPUT_FILENAME = "musiclist_for_soundiiz.txt"  # Ausgabe-Datei im TXT-Format mit Titel-Künstler-Album

if MUSICLISTFORSOUNDIIZ_LOGGING_ENABLED:
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
else:
    logging.basicConfig(level=logging.CRITICAL)


def musiclistforsoundiizMain():
    """
    Hauptfunktion: Scannt das Verzeichnis, extrahiert Metadaten und schreibt mehrere CSV-Dateien und eine TXT-Datei für Soundiiz.
    """
    logging.debug(f"Starte Scan des Verzeichnisses: {MUSICLISTFORSOUNDIIZ_DIRECTORY_TO_SCAN}")
    try:
        musikdateien = musiclistforsoundiizGetMusicFiles(MUSICLISTFORSOUNDIIZ_DIRECTORY_TO_SCAN)
        logging.debug(f"Gefundene Musikdateien: {len(musikdateien)}")

        # TXT-Datei öffnen zum Schreiben
        with open(MUSICLISTFORSOUNDIIZ_TXT_OUTPUT_FILENAME, "w", encoding="utf-8") as txt_datei:
            csv_file_index = 1
            csv_song_count = 0
            csv_datei = None

            def open_new_csv():
                nonlocal csv_datei
                filename = f"{MUSICLISTFORSOUNDIIZ_OUTPUT_FILENAME_BASE}{csv_file_index}{MUSICLISTFORSOUNDIIZ_OUTPUT_FILE_EXTENSION}"
                logging.debug(f"Öffne neue CSV-Datei: {filename}")
                f = open(filename, "w", encoding="utf-8")
                # Header gemäß Soundiiz-Spezifikation mit abschließendem Komma: title,artist,album,isrc,
                f.write("title,artist,album,isrc,\n")
                return f

            # erste CSV-Datei öffnen
            csv_datei = open_new_csv()

            for dateipfad in musikdateien:
                try:
                    artist, title, album = musiclistforsoundiizExtractMetadata(dateipfad)
                    # CSV-konforme Ausgabe (Escape von Kommas und Anführungszeichen)
                    artist_csv = musiclistforsoundiizEscapeCSV(artist)
                    title_csv = musiclistforsoundiizEscapeCSV(title)
                    album_csv = musiclistforsoundiizEscapeCSV(album)
                    # isrc-Feld leer lassen (Soundiiz Empfehlung)
                    zeile_csv = f"{title_csv},{artist_csv},{album_csv},,\n"
                    csv_datei.write(zeile_csv)
                    logging.debug(f"Schrieb CSV-Zeile: {zeile_csv.strip()}")

                    # TXT-Ausgabe: Titel - Künstler - Album
                    zeile_txt = f"{title} - {artist}\n"
                    txt_datei.write(zeile_txt)
                    logging.debug(f"Schrieb TXT-Zeile: {zeile_txt.strip()}")

                    csv_song_count += 1
                    # Prüfen, ob neue CSV-Datei geöffnet werden muss
                    if csv_song_count >= MUSICLISTFORSOUNDIIZ_MAX_SONGS_PER_FILE:
                        csv_datei.close()
                        logging.info(f"CSV-Datei '{MUSICLISTFORSOUNDIIZ_OUTPUT_FILENAME_BASE}{csv_file_index}{MUSICLISTFORSOUNDIIZ_OUTPUT_FILE_EXTENSION}' fertig mit {csv_song_count} Songs.")
                        csv_file_index += 1
                        csv_song_count = 0
                        csv_datei = open_new_csv()

                except Exception as e:
                    logging.error(f"Fehler bei Datei {dateipfad}: {e}")

            if csv_datei and not csv_datei.closed:
                csv_datei.close()
                logging.info(f"CSV-Datei '{MUSICLISTFORSOUNDIIZ_OUTPUT_FILENAME_BASE}{csv_file_index}{MUSICLISTFORSOUNDIIZ_OUTPUT_FILE_EXTENSION}' fertig mit {csv_song_count} Songs.")

        logging.info(f"TXT-Datei '{MUSICLISTFORSOUNDIIZ_TXT_OUTPUT_FILENAME}' erfolgreich erstellt.")

    except Exception as e:
        logging.error(f"Fehler im Hauptprozess: {e}")


def musiclistforsoundiizGetMusicFiles(verzeichnis):
    """
    Findet rekursiv alle unterstützten Musikdateien im Verzeichnis.
    """
    dateien = []
    for root, _, files in os.walk(verzeichnis):
        for file in files:
            if any(file.lower().endswith(ext) for ext in MUSICLISTFORSOUNDIIZ_SUPPORTED_EXTENSIONS):
                vollpfad = os.path.join(root, file)
                dateien.append(vollpfad)
                logging.debug(f"Gefundene Datei: {vollpfad}")
    return dateien


def musiclistforsoundiizExtractMetadata(dateipfad):
    """
    Liest Metadaten (Artist, Title, Album) aus Musikdatei mit mutagen.
    Falls der Titel nicht gefunden wird oder aus dem Dateinamen extrahiert wird,
    wird der Dateiname im Format 'Artist - Title' geparst und bevorzugt gegenüber Metadaten verwendet.
    """
    from mutagen import File
    logging.debug(f"Lese Metadaten aus: {dateipfad}")
    audio = File(dateipfad, easy=True)
    if audio is None:
        raise ValueError("Datei nicht lesbar oder nicht unterstütztes Format")

    artist_meta = musiclistforsoundiizSafeGetFirst(audio, ["artist", "albumartist", "performer"]) or None
    title_meta = musiclistforsoundiizSafeGetFirst(audio, ["title"]) or None
    album = musiclistforsoundiizSafeGetFirst(audio, ["album"]) or "Unbekanntes Album"

    # Versuche Titel und Artist aus Dateiname zu extrahieren und diesen zu bevorzugen
    basename = os.path.splitext(os.path.basename(dateipfad))[0]  # ohne Dateiendung
    logging.debug(f"Versuche Parsing aus Dateiname: '{basename}'")
    if " - " in basename:
        parts = basename.split(" - ", 1)
        if len(parts) == 2:
            artist_file = parts[0].strip()
            title_file = parts[1].strip()
            logging.debug(f"Aus Dateiname extrahiert - Artist: '{artist_file}', Title: '{title_file}'")
        else:
            artist_file = None
            title_file = basename.strip()
            logging.debug(f"Parsing unklar, setze Titel auf Dateinamen: '{title_file}'")
    else:
        artist_file = None
        title_file = basename.strip()
        logging.debug(f"Kein Trennzeichen im Dateinamen, setze Titel auf Dateinamen: '{title_file}'")

    # Bevorzuge den aus dem Dateinamen extrahierten Titel und Artist, falls vorhanden
    artist = artist_file if artist_file else (artist_meta if artist_meta else "Unbekannter Künstler")
    title = title_file if title_file else (title_meta if title_meta else basename.strip())

    return artist, title, album


def musiclistforsoundiizSafeGetFirst(audio, keys):
    """
    Hilfsfunktion: Gibt ersten nicht-leeren Wert aus Audio Tags zurück.
    """
    for key in keys:
        if key in audio and audio[key]:
            wert = audio[key][0]
            if isinstance(wert, bytes):
                wert = wert.decode("utf-8", errors="ignore")
            wert_stripped = wert.strip()
            if wert_stripped:
                return wert_stripped
    return None


def musiclistforsoundiizEscapeCSV(text):
    """
    Escaped CSV-Werte gemäß RFC: Wenn Komma oder Anführungszeichen enthalten sind,
    wird der Wert in Anführungszeichen gesetzt und interne Anführungszeichen verdoppelt.
    """
    if any(c in text for c in ['"', ',']):
        text = text.replace('"', '""')
        return f'"{text}"'
    else:
        return text


if __name__ == "__main__":
    musiclistforsoundiizMain()
