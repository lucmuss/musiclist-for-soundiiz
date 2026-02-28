"""Integration tests for scanner views."""

import pytest
from django.urls import reverse

from scanner.models import ScanSession, MusicFile


@pytest.mark.integration
@pytest.mark.django_db
class TestScannerViews:
    """Test scanner app views."""

    def test_scan_list_view(self, client, scan_session):
        """Test scan list view."""
        response = client.get(reverse("scanner:scan_list"))
        assert response.status_code == 200
        assert "scan" in response.content.decode().lower()

    def test_scan_detail_view(self, client, scan_session):
        """Test scan detail view."""
        response = client.get(reverse("scanner:scan_detail", kwargs={"pk": scan_session.pk}))
        assert response.status_code == 200
        assert scan_session.name in response.content.decode()

    def test_scan_upload_view_get(self, client):
        """Test scan upload view GET."""
        response = client.get(reverse("scanner:scan_upload"))
        assert response.status_code == 200

    def test_scan_upload_view_post_invalid_path(self, client):
        """Test scan upload with invalid path."""
        response = client.post(reverse("scanner:scan_upload"), {
            "directory_path": "/nonexistent/path",
            "session_name": "Test",
        })
        assert response.status_code == 200
        # Should show error message
        content = response.content.decode()
        assert "error" in content.lower() or "not found" in content.lower()

    def test_music_file_detail_view(self, client, music_file):
        """Test music file detail view."""
        response = client.get(reverse("scanner:music_file_detail", kwargs={"pk": music_file.pk}))
        assert response.status_code == 200
        assert music_file.title in response.content.decode()

    def test_scan_delete_view(self, client, scan_session):
        """Test scan delete view."""
        count_before = ScanSession.objects.count()
        response = client.post(reverse("scanner:scan_delete", kwargs={"pk": scan_session.pk}))
        assert response.status_code == 302  # Redirect
        assert ScanSession.objects.count() == count_before - 1
