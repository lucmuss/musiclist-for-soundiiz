"""Integration tests for core views."""

import pytest
from django.urls import reverse


@pytest.mark.integration
@pytest.mark.django_db
class TestCoreViews:
    """Test core app views."""

    def test_home_view(self, client):
        """Test home page view."""
        response = client.get(reverse("core:home"))
        assert response.status_code == 200
        assert "MusicList" in response.content.decode()

    def test_health_check_view(self, client):
        """Test health check endpoint."""
        response = client.get(reverse("core:health_check"))
        assert response.status_code == 200
        assert response.content.decode() == "OK"
