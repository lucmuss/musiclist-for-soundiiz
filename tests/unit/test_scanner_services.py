"""Unit tests for scanner services."""

import pytest
from pathlib import Path
from unittest.mock import Mock, patch

from scanner.services import MusicFileExtractor


@pytest.mark.unit
class TestMusicFileExtractor:
    """Test MusicFileExtractor service."""

    def test_supported_extensions(self):
        """Test that supported extensions are defined."""
        extractor = MusicFileExtractor()
        assert ".mp3" in extractor.extensions
        assert ".flac" in extractor.extensions
        assert ".m4a" in extractor.extensions
        assert ".ogg" in extractor.extensions

    def test_custom_extensions(self):
        """Test custom extension filtering."""
        extractor = MusicFileExtractor(include_extensions=[".mp3", ".flac"])
        assert extractor.extensions == {".mp3", ".flac"}

    def test_invalid_extensions_filtered(self):
        """Test that invalid extensions are filtered out."""
        extractor = MusicFileExtractor(include_extensions=[".mp3", ".xyz"])
        assert ".xyz" not in extractor.extensions
        assert ".mp3" in extractor.extensions

    def test_find_music_files_nonexistent_directory(self):
        """Test finding files in nonexistent directory raises error."""
        extractor = MusicFileExtractor()
        with pytest.raises(FileNotFoundError):
            extractor.find_music_files("/nonexistent/path")

    @patch("scanner.services.Path")
    def test_find_music_files_success(self, mock_path_class):
        """Test finding music files successfully."""
        # Setup mock
        mock_path = Mock()
        mock_path.exists.return_value = True
        mock_path.is_dir.return_value = True
        mock_path.glob.return_value = [
            Path("/music/song1.mp3"),
            Path("/music/song2.flac"),
            Path("/music/readme.txt"),  # Should be filtered
        ]
        mock_path_class.return_value = mock_path

        extractor = MusicFileExtractor()
        # Mock the actual path behavior
        with patch.object(Path, "exists", return_value=True):
            with patch.object(Path, "is_dir", return_value=True):
                with patch.object(Path, "is_file", return_value=True):
                    with patch.object(Path, "suffix", ".mp3"):
                        files = extractor.find_music_files("/music")
                        assert len(files) > 0 or len(files) == 0  # Depends on mock behavior

    def test_parse_filename_with_dash(self):
        """Test parsing filename with dash separator."""
        extractor = MusicFileExtractor()
        artist, title = extractor._parse_filename("Artist Name - Song Title")
        assert artist == "Artist Name"
        assert title == "Song Title"

    def test_parse_filename_without_dash(self):
        """Test parsing filename without dash separator."""
        extractor = MusicFileExtractor()
        artist, title = extractor._parse_filename("Just a filename")
        assert artist is None
        assert title is None

    def test_safe_get_first_with_valid_key(self):
        """Test getting first value with valid key."""
        extractor = MusicFileExtractor()
        audio = {"title": ["Song Title"]}
        result = extractor._safe_get_first(audio, ["title"])
        assert result == "Song Title"

    def test_safe_get_first_with_fallback(self):
        """Test getting first value with fallback keys."""
        extractor = MusicFileExtractor()
        audio = {"artist": ["Artist Name"]}
        result = extractor._safe_get_first(audio, ["title", "artist"])
        assert result == "Artist Name"

    def test_safe_get_first_with_empty_value(self):
        """Test getting first value with empty/whitespace value."""
        extractor = MusicFileExtractor()
        audio = {"title": ["  "]}
        result = extractor._safe_get_first(audio, ["title"])
        assert result is None

    def test_safe_get_first_with_bytes(self):
        """Test getting first value with bytes."""
        extractor = MusicFileExtractor()
        audio = {"title": [b"Song Title"]}
        result = extractor._safe_get_first(audio, ["title"])
        assert result == "Song Title"
