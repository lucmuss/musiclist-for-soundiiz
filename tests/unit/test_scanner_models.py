"""Unit tests for scanner models."""

import pytest
from datetime import datetime, timezone

from scanner.models import ScanSession, MusicFile


@pytest.mark.unit
class TestScanSession:
    """Test ScanSession model."""

    def test_str_with_name(self):
        """Test string representation with name."""
        session = ScanSession(name="My Scan", status="completed")
        assert "My Scan" in str(session)
        assert "completed" in str(session)

    def test_str_without_name(self):
        """Test string representation without name."""
        session = ScanSession(status="pending")
        session.created_at = datetime(2024, 1, 1, 12, 0, tzinfo=timezone.utc)
        result = str(session)
        assert "Scan" in result
        assert "pending" in result

    def test_success_rate_with_files(self):
        """Test success rate calculation."""
        session = ScanSession(total_files_found=100, total_files_processed=75)
        assert session.success_rate == 75.0

    def test_success_rate_zero_files(self):
        """Test success rate with zero files."""
        session = ScanSession(total_files_found=0)
        assert session.success_rate == 0.0


@pytest.mark.unit
class TestMusicFile:
    """Test MusicFile model."""

    def test_str_with_title_and_artist(self):
        """Test string representation with title and artist."""
        file = MusicFile(title="My Song", artist="My Artist", filename="song.mp3")
        assert str(file) == "My Artist - My Song"

    def test_str_without_metadata(self):
        """Test string representation without metadata."""
        file = MusicFile(filename="song.mp3")
        assert str(file) == "song.mp3"

    def test_duration_formatted_with_seconds(self):
        """Test duration formatting."""
        file = MusicFile(duration=185)
        assert file.duration_formatted == "3:05"

    def test_duration_formatted_zero(self):
        """Test duration formatting for zero duration."""
        file = MusicFile(duration=0)
        assert file.duration_formatted == "--:--"

    def test_has_metadata_true(self):
        """Test has_metadata with metadata."""
        file = MusicFile(title="Song", artist="Artist")
        assert file.has_metadata is True

    def test_has_metadata_false(self):
        """Test has_metadata without metadata."""
        file = MusicFile()
        assert file.has_metadata is False
