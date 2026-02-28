"""Integration tests for export views."""

import os

import pytest
from django.urls import reverse

from exports.models import ExportJob


@pytest.mark.integration
@pytest.mark.django_db
class TestExportViews:
    """Test export app views."""

    def test_export_list_view(self, client, export_job):
        """Test export list view."""
        response = client.get(reverse("exports:export_list"))
        assert response.status_code == 200

    def test_export_create_view_get(self, client, playlist):
        """Test export create view GET."""
        response = client.get(reverse("exports:export_create", kwargs={"playlist_pk": playlist.pk}))
        assert response.status_code == 200
        assert playlist.name in response.content.decode()

    def test_export_create_view_post(self, client, playlist, playlist_item, tmp_path, settings):
        """Test export create view POST."""
        # Setup media root for test
        settings.MEDIA_ROOT = str(tmp_path)

        response = client.post(
            reverse("exports:export_create", kwargs={"playlist_pk": playlist.pk}),
            {"format_type": "csv"},
        )
        assert response.status_code == 302  # Redirects to download view

    def test_export_delete_view(self, client, export_job):
        """Test export delete view."""
        count_before = ExportJob.objects.count()
        response = client.post(reverse("exports:export_delete", kwargs={"pk": export_job.pk}))
        assert response.status_code == 302
        assert ExportJob.objects.count() == count_before - 1
