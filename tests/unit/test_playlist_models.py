"""Unit tests for playlist models."""

import pytest
from unittest.mock import Mock, patch

from playlists.models import Playlist, PlaylistItem
from scanner.models import MusicFile


@pytest.mark.unit
class TestPlaylist:
    """Test Playlist model."""

    def test_str(self):
        """Test string representation."""
        playlist = Playlist(name="My Playlist")
        assert str(playlist) == "My Playlist"

    def test_total_tracks(self):
        """Test total tracks count."""
        playlist = Playlist(name="Test")
        playlist.save()

        # Create mock items
        with patch.object(playlist, 'items') as mock_items:
            mock_items.count.return_value = 5
            assert playlist.total_tracks == 5

    def test_total_duration(self):
        """Test total duration calculation."""
        playlist = Playlist(name="Test")
        playlist.save()

        # Mock items with music files having durations
        mock_item1 = Mock()
        mock_item1.music_file.duration = 180
        mock_item2 = Mock()
        mock_item2.music_file.duration = 240

        with patch.object(playlist, 'items') as mock_items:
            mock_items.all.return_value = [mock_item1, mock_item2]
            assert playlist.total_duration == 420

    def test_duration_formatted_hours(self):
        """Test duration formatted with hours."""
        playlist = Playlist(name="Test")
        with patch.object(playlist, 'total_duration', 3665):
            assert playlist.duration_formatted == "1:01:05"

    def test_duration_formatted_minutes(self):
        """Test duration formatted with only minutes."""
        playlist = Playlist(name="Test")
        with patch.object(playlist, 'total_duration', 185):
            assert playlist.duration_formatted == "3:05"

    def test_duration_formatted_zero(self):
        """Test duration formatted for zero."""
        playlist = Playlist(name="Test")
        with patch.object(playlist, 'total_duration', 0):
            assert playlist.duration_formatted == "0:00"


@pytest.mark.unit
class TestPlaylistItem:
    """Test PlaylistItem model."""

    def test_str(self):
        """Test string representation."""
        playlist = Playlist(name="Test Playlist")
        music_file = MusicFile(title="Song", artist="Artist")
        item = PlaylistItem(playlist=playlist, music_file=music_file, position=0)
        assert "1." in str(item)
        assert "Artist - Song" in str(item)
