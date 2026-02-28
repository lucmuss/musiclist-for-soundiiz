"""Unit tests for export services."""

import json
import os
from pathlib import Path

import pytest

from exports.services import (
    CSVExporter,
    JSONExporter,
    M3UExporter,
    TXTExporter,
    get_exporter,
)


@pytest.mark.unit
class TestCSVExporter:
    """Test CSV export functionality."""

    def test_export_creates_file(self, tmp_path):
        """Test that export creates a file."""
        exporter = CSVExporter()
        tracks = [
            {"title": "Song 1", "artist": "Artist 1", "album": "Album 1", "isrc": "ISRC1"},
            {"title": "Song 2", "artist": "Artist 2", "album": "Album 2", "isrc": ""},
        ]
        output_path = tmp_path / "test.csv"
        result = exporter.export(tracks, str(output_path))
        assert Path(result).exists()

    def test_export_content_format(self, tmp_path):
        """Test CSV export content format."""
        exporter = CSVExporter()
        tracks = [{"title": "Song", "artist": "Artist", "album": "Album", "isrc": "ISRC"}]
        output_path = tmp_path / "test.csv"
        exporter.export(tracks, str(output_path))

        with open(output_path) as f:
            lines = f.readlines()
        assert lines[0].strip() == "title,artist,album,isrc,"
        assert "Song,Artist,Album,ISRC," in lines[1]

    def test_escape_csv_with_comma(self):
        """Test CSV escaping with comma."""
        exporter = CSVExporter()
        result = exporter._escape_csv("Artist, The")
        assert result == '"Artist, The"'

    def test_escape_csv_with_quote(self):
        """Test CSV escaping with quote."""
        exporter = CSVExporter()
        result = exporter._escape_csv('Artist "The" Band')
        assert result == '"Artist ""The"" Band"'


@pytest.mark.unit
class TestJSONExporter:
    """Test JSON export functionality."""

    def test_export_creates_file(self, tmp_path):
        """Test that export creates a file."""
        exporter = JSONExporter()
        tracks = [{"title": "Song", "artist": "Artist", "album": "Album"}]
        output_path = tmp_path / "test.json"
        result = exporter.export(tracks, str(output_path))
        assert Path(result).exists()

    def test_export_content_structure(self, tmp_path):
        """Test JSON export content structure."""
        exporter = JSONExporter()
        tracks = [{"title": "Song", "artist": "Artist"}]
        output_path = tmp_path / "test.json"
        exporter.export(tracks, str(output_path))

        with open(output_path) as f:
            data = json.load(f)
        assert "tracks" in data
        assert "total_tracks" in data
        assert data["total_tracks"] == 1


@pytest.mark.unit
class TestM3UExporter:
    """Test M3U export functionality."""

    def test_export_creates_file(self, tmp_path):
        """Test that export creates a file."""
        exporter = M3UExporter()
        tracks = [{"title": "Song", "artist": "Artist", "file_path": "/music/song.mp3"}]
        output_path = tmp_path / "test.m3u"
        result = exporter.export(tracks, str(output_path))
        assert Path(result).exists()

    def test_export_extended_format(self, tmp_path):
        """Test M3U extended format."""
        exporter = M3UExporter(extended=True)
        tracks = [
            {"title": "Song", "artist": "Artist", "duration": 180, "file_path": "/music/song.mp3"}
        ]
        output_path = tmp_path / "test.m3u"
        exporter.export(tracks, str(output_path))

        with open(output_path) as f:
            content = f.read()
        assert "#EXTM3U" in content
        assert "#EXTINF:180,Artist - Song" in content


@pytest.mark.unit
class TestTXTExporter:
    """Test TXT export functionality."""

    def test_export_creates_file(self, tmp_path):
        """Test that export creates a file."""
        exporter = TXTExporter()
        tracks = [{"title": "Song", "artist": "Artist"}]
        output_path = tmp_path / "test.txt"
        result = exporter.export(tracks, str(output_path))
        assert Path(result).exists()

    def test_export_format(self, tmp_path):
        """Test TXT export format."""
        exporter = TXTExporter()
        tracks = [{"title": "My Song", "artist": "My Artist"}]
        output_path = tmp_path / "test.txt"
        exporter.export(tracks, str(output_path))

        with open(output_path) as f:
            content = f.read()
        assert "My Song - My Artist" in content


@pytest.mark.unit
class TestGetExporter:
    """Test get_exporter factory function."""

    def test_get_csv_exporter(self):
        """Test getting CSV exporter."""
        exporter = get_exporter("csv")
        assert isinstance(exporter, CSVExporter)

    def test_get_json_exporter(self):
        """Test getting JSON exporter."""
        exporter = get_exporter("json")
        assert isinstance(exporter, JSONExporter)

    def test_get_m3u_exporter(self):
        """Test getting M3U exporter."""
        exporter = get_exporter("m3u")
        assert isinstance(exporter, M3UExporter)

    def test_get_txt_exporter(self):
        """Test getting TXT exporter."""
        exporter = get_exporter("txt")
        assert isinstance(exporter, TXTExporter)

    def test_get_exporter_case_insensitive(self):
        """Test that format is case insensitive."""
        exporter = get_exporter("CSV")
        assert isinstance(exporter, CSVExporter)

    def test_get_exporter_invalid_format(self):
        """Test that invalid format raises error."""
        with pytest.raises(ValueError, match="Unsupported format"):
            get_exporter("invalid")
