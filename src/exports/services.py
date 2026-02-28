# -*- coding: utf-8 -*-
"""Export services for playlist formats."""

import csv
import json
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, Type

logger = logging.getLogger(__name__)


class BaseExporter(ABC):
    """Base class for playlist exporters."""

    @abstractmethod
    def export(self, tracks: List[Dict[str, Any]], output_path: str) -> str:
        """
        Export tracks to a file.

        Args:
            tracks: List of track dictionaries with metadata
            output_path: Path to the output file

        Returns:
            Path to the exported file
        """
        pass


class CSVExporter(BaseExporter):
    """Export playlist to CSV format compatible with Soundiiz."""

    def export(self, tracks: List[Dict[str, Any]], output_path: str) -> str:
        """
        Export tracks to CSV in Soundiiz format.
        Format: title,artist,album,isrc,
        Note: The trailing comma is intentional per Soundiiz specification.
        """
        output_path_obj = Path(output_path)
        output_path_obj.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path_obj, "w", encoding="utf-8", newline="") as csvfile:
            # Soundiiz CSV header with trailing comma
            csvfile.write("title,artist,album,isrc,\n")

            for track in tracks:
                title = self._escape_csv(track.get("title", ""))
                artist = self._escape_csv(track.get("artist", ""))
                album = self._escape_csv(track.get("album", ""))
                isrc = self._escape_csv(track.get("isrc", ""))

                # Write row with trailing comma
                csvfile.write(f"{title},{artist},{album},{isrc},\n")

        logger.info(f"Exported {len(tracks)} tracks to CSV: {output_path}")
        return str(output_path_obj)

    @staticmethod
    def _escape_csv(text: str) -> str:
        """Escape CSV values according to RFC 4180."""
        if any(c in text for c in ['"', ","]):
            text = text.replace('"', '""')
            return f'"{text}"'
        return text


class JSONExporter(BaseExporter):
    """Export playlist to JSON format."""

    def __init__(self, pretty: bool = True):
        self.pretty = pretty

    def export(self, tracks: List[Dict[str, Any]], output_path: str) -> str:
        """Export tracks to JSON file."""
        output_path_obj = Path(output_path)
        output_path_obj.parent.mkdir(parents=True, exist_ok=True)

        export_data = {
            "playlist_name": tracks[0].get("playlist_name", "Unknown Playlist") if tracks else "Unknown Playlist",
            "total_tracks": len(tracks),
            "tracks": tracks,
        }

        with open(output_path_obj, "w", encoding="utf-8") as jsonfile:
            if self.pretty:
                json.dump(export_data, jsonfile, indent=2, ensure_ascii=False)
            else:
                json.dump(export_data, jsonfile, ensure_ascii=False)

        logger.info(f"Exported {len(tracks)} tracks to JSON: {output_path}")
        return str(output_path_obj)


class M3UExporter(BaseExporter):
    """Export playlist to M3U format."""

    def __init__(self, extended: bool = True):
        self.extended = extended

    def export(self, tracks: List[Dict[str, Any]], output_path: str) -> str:
        """Export tracks to M3U playlist file."""
        output_path_obj = Path(output_path)
        output_path_obj.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path_obj, "w", encoding="utf-8") as m3ufile:
            if self.extended:
                m3ufile.write("#EXTM3U\n")

            for track in tracks:
                if self.extended:
                    duration = track.get("duration", -1) or -1
                    artist = track.get("artist", "Unknown Artist")
                    title = track.get("title", "Unknown Title")
                    m3ufile.write(f"#EXTINF:{duration},{artist} - {title}\n")

                file_path = track.get("file_path", "")
                m3ufile.write(f"{file_path}\n")

        logger.info(f"Exported {len(tracks)} tracks to M3U: {output_path}")
        return str(output_path_obj)


class TXTExporter(BaseExporter):
    """Export playlist to simple text format."""

    def export(self, tracks: List[Dict[str, Any]], output_path: str) -> str:
        """Export tracks to text file (format: Title - Artist)."""
        output_path_obj = Path(output_path)
        output_path_obj.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path_obj, "w", encoding="utf-8") as txtfile:
            for track in tracks:
                title = track.get("title", "Unknown Title")
                artist = track.get("artist", "Unknown Artist")
                txtfile.write(f"{title} - {artist}\n")

        logger.info(f"Exported {len(tracks)} tracks to TXT: {output_path}")
        return str(output_path_obj)


def get_exporter(format_type: str, **kwargs) -> BaseExporter:
    """
    Get exporter instance for the specified format.

    Args:
        format_type: Export format (csv, json, m3u, txt)
        **kwargs: Additional arguments for the exporter

    Returns:
        Exporter instance

    Raises:
        ValueError: If format is not supported
    """
    format_type = format_type.lower()

    exporters: Dict[str, Type[BaseExporter]] = {
        "csv": CSVExporter,
        "json": JSONExporter,
        "m3u": M3UExporter,
        "txt": TXTExporter,
    }

    if format_type not in exporters:
        raise ValueError(
            f"Unsupported format: {format_type}. "
            f"Supported formats: {', '.join(exporters.keys())}"
        )

    return exporters[format_type](**kwargs)


def export_playlist(playlist, format_type: str, output_dir: str) -> str:
    """
    Export a playlist to the specified format.

    Args:
        playlist: Playlist model instance
        format_type: Export format (csv, json, m3u, txt)
        output_dir: Directory to save the export file

    Returns:
        Path to the exported file
    """
    # Get tracks from playlist
    tracks = []
    for item in playlist.items.select_related("music_file").all():
        music_file = item.music_file
        tracks.append({
            "title": music_file.title,
            "artist": music_file.artist,
            "album": music_file.album,
            "isrc": music_file.isrc,
            "genre": music_file.genre,
            "year": music_file.year,
            "duration": music_file.duration,
            "file_path": music_file.file_path,
            "filename": music_file.filename,
            "playlist_name": playlist.name,
        })

    # Generate output filename
    safe_name = "".join(c for c in playlist.name if c.isalnum() or c in " -_").strip()
    output_path = Path(output_dir) / f"{safe_name}.{format_type}"

    # Export
    exporter = get_exporter(format_type)
    return exporter.export(tracks, str(output_path))
