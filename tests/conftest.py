"""Test configuration and fixtures."""

import pytest
from django.test import Client

from exports.models import ExportJob
from playlists.models import Playlist, PlaylistItem
from scanner.models import MusicFile, ScanSession


@pytest.fixture
def client():
    """Provide a test client."""
    return Client()


@pytest.fixture
def scan_session():
    """Create a test scan session."""
    return ScanSession.objects.create(
        name="Test Scan",
        source_path="/test/music",
        recursive=True,
        status="completed",
        total_files_found=10,
        total_files_processed=10,
    )


@pytest.fixture
def music_file(scan_session):
    """Create a test music file."""
    return MusicFile.objects.create(
        scan_session=scan_session,
        file_path="/test/music/song.mp3",
        filename="song.mp3",
        title="Test Song",
        artist="Test Artist",
        album="Test Album",
        isrc="USXXX1234567",
        genre="Rock",
        year="2024",
        duration=180,
        processed=True,
    )


@pytest.fixture
def playlist():
    """Create a test playlist."""
    return Playlist.objects.create(
        name="Test Playlist",
        description="A test playlist",
    )


@pytest.fixture
def playlist_item(playlist, music_file):
    """Create a test playlist item."""
    return PlaylistItem.objects.create(
        playlist=playlist,
        music_file=music_file,
        position=0,
    )


@pytest.fixture
def export_job(playlist):
    """Create a test export job."""
    return ExportJob.objects.create(
        playlist=playlist,
        format_type="csv",
        status="completed",
        file_path="/tmp/test.csv",
    )
