from django.db import models
from core.models import BaseModel
from playlists.models import Playlist


class ExportJob(BaseModel):
    """Represents an export job for a playlist."""

    FORMAT_CHOICES = [
        ("csv", "CSV (Soundiiz)"),
        ("json", "JSON"),
        ("m3u", "M3U Playlist"),
        ("txt", "TXT (Simple Text)"),
    ]

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ]

    playlist = models.ForeignKey(
        Playlist,
        on_delete=models.CASCADE,
        related_name="export_jobs",
    )
    format_type = models.CharField(max_length=10, choices=FORMAT_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    file_path = models.CharField(max_length=1024, blank=True)
    error_message = models.TextField(blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Export Job"
        verbose_name_plural = "Export Jobs"

    def __str__(self) -> str:
        return f"{self.playlist.name} - {self.get_format_type_display()} ({self.status})"

    @property
    def filename(self) -> str:
        """Generate filename for export."""
        safe_name = "".join(c for c in self.playlist.name if c.isalnum() or c in " -_").strip()
        return f"{safe_name}.{self.format_type}"
