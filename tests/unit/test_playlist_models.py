"""Unit tests for playlist models."""

from unittest.mock import Mock, PropertyMock, patch

import pytest

from playlists.models import Playlist, PlaylistItem
from scanner.models import MusicFile, ScanSession


@pytest.mark.unit
@pytest.mark.django_db
class TestPlaylist:
    """Test Playlist model."""

    def test_str(self):
        """Test string representation."""
        playlist = Playlist(name="My Playlist")
        assert str(playlist) == "My Playlist"

    def test_total_tracks(self):
        """Test total tracks count."""
        scan_session = ScanSession.objects.create(
            source_path="/tmp/music",
            status="completed",
            total_files_found=2,
            total_files_processed=2,
        )
        playlist = Playlist.objects.create(name="Test")
        music_file_1 = MusicFile.objects.create(
            scan_session=scan_session,
            file_path="/tmp/music/song1.mp3",
            filename="song1.mp3",
            duration=180,
        )
        music_file_2 = MusicFile.objects.create(
            scan_session=scan_session,
            file_path="/tmp/music/song2.mp3",
            filename="song2.mp3",
            duration=240,
        )
        PlaylistItem.objects.create(playlist=playlist, music_file=music_file_1, position=0)
        PlaylistItem.objects.create(playlist=playlist, music_file=music_file_2, position=1)

        assert playlist.total_tracks == 2

    def test_total_duration(self):
        """Test total duration calculation."""
        scan_session = ScanSession.objects.create(
            source_path="/tmp/music",
            status="completed",
            total_files_found=2,
            total_files_processed=2,
        )
        playlist = Playlist.objects.create(name="Test")
        music_file_1 = MusicFile.objects.create(
            scan_session=scan_session,
            file_path="/tmp/music/song1.mp3",
            filename="song1.mp3",
            duration=180,
        )
        music_file_2 = MusicFile.objects.create(
            scan_session=scan_session,
            file_path="/tmp/music/song2.mp3",
            filename="song2.mp3",
            duration=240,
        )
        PlaylistItem.objects.create(playlist=playlist, music_file=music_file_1, position=0)
        PlaylistItem.objects.create(playlist=playlist, music_file=music_file_2, position=1)

        assert playlist.total_duration == 420

    def test_duration_formatted_hours(self):
        """Test duration formatted with hours."""
        playlist = Playlist(name="Test")
        with patch.object(Playlist, "total_duration", new_callable=PropertyMock) as mock_duration:
            mock_duration.return_value = 3665
            assert playlist.duration_formatted == "1:01:05"

    def test_duration_formatted_minutes(self):
        """Test duration formatted with only minutes."""
        playlist = Playlist(name="Test")
        with patch.object(Playlist, "total_duration", new_callable=PropertyMock) as mock_duration:
            mock_duration.return_value = 185
            assert playlist.duration_formatted == "3:05"

    def test_duration_formatted_zero(self):
        """Test duration formatted for zero."""
        playlist = Playlist(name="Test")
        with patch.object(Playlist, "total_duration", new_callable=PropertyMock) as mock_duration:
            mock_duration.return_value = 0
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
