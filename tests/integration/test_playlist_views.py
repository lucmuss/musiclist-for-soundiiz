"""Integration tests for playlist views."""

import pytest
from django.urls import reverse

from playlists.models import Playlist, PlaylistItem
from scanner.models import MusicFile


@pytest.mark.integration
@pytest.mark.django_db
class TestPlaylistViews:
    """Test playlist app views."""

    def test_playlist_list_view(self, client, playlist):
        """Test playlist list view."""
        response = client.get(reverse("playlists:playlist_list"))
        assert response.status_code == 200
        assert playlist.name in response.content.decode()

    def test_playlist_detail_view(self, client, playlist):
        """Test playlist detail view."""
        response = client.get(reverse("playlists:playlist_detail", kwargs={"pk": playlist.pk}))
        assert response.status_code == 200
        assert playlist.name in response.content.decode()

    def test_playlist_create_view_get(self, client):
        """Test playlist create view GET."""
        response = client.get(reverse("playlists:playlist_create"))
        assert response.status_code == 200

    def test_playlist_create_view_post(self, client):
        """Test playlist create view POST."""
        response = client.post(
            reverse("playlists:playlist_create"),
            {
                "name": "New Playlist",
                "description": "Test description",
            },
        )
        assert response.status_code == 302  # Redirect
        assert Playlist.objects.filter(name="New Playlist").exists()

    def test_playlist_edit_view(self, client, playlist):
        """Test playlist edit view."""
        response = client.post(
            reverse("playlists:playlist_edit", kwargs={"pk": playlist.pk}),
            {
                "name": "Updated Name",
                "description": "Updated description",
            },
        )
        assert response.status_code == 302
        playlist.refresh_from_db()
        assert playlist.name == "Updated Name"

    def test_playlist_delete_view(self, client, playlist):
        """Test playlist delete view."""
        count_before = Playlist.objects.count()
        response = client.post(reverse("playlists:playlist_delete", kwargs={"pk": playlist.pk}))
        assert response.status_code == 302
        assert Playlist.objects.count() == count_before - 1

    def test_playlist_add_tracks_view(self, client, playlist, music_file):
        """Test playlist add tracks view."""
        response = client.get(reverse("playlists:playlist_add_tracks", kwargs={"pk": playlist.pk}))
        assert response.status_code == 200

    def test_playlist_add_tracks_post(self, client, playlist, music_file):
        """Test adding tracks to playlist."""
        response = client.post(
            reverse("playlists:playlist_add_tracks", kwargs={"pk": playlist.pk}),
            {"music_files": [str(music_file.pk)]},
        )
        assert response.status_code == 302
        assert playlist.items.filter(music_file=music_file).exists()

    def test_playlist_remove_track(self, client, playlist, playlist_item):
        """Test removing track from playlist."""
        response = client.post(
            reverse(
                "playlists:playlist_remove_track",
                kwargs={"playlist_pk": playlist.pk, "item_pk": playlist_item.pk},
            )
        )
        assert response.status_code == 302
        assert not playlist.items.filter(pk=playlist_item.pk).exists()
