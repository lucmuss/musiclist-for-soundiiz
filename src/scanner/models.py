from django.db import models
from django.core.validators import MinValueValidator
from core.models import BaseModel


class ScanSession(BaseModel):
    """Represents a music scanning session."""

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("scanning", "Scanning"),
        ("completed", "Completed"),
        ("failed", "Failed"),
    ]

    name = models.CharField(max_length=255, blank=True, help_text="Optional name for this scan session")
    source_path = models.CharField(max_length=1024, help_text="Path to the scanned directory")
    recursive = models.BooleanField(default=True, help_text="Whether subdirectories were scanned")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    total_files_found = models.PositiveIntegerField(default=0)
    total_files_processed = models.PositiveIntegerField(default=0)
    total_files_failed = models.PositiveIntegerField(default=0)
    error_message = models.TextField(blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Scan Session"
        verbose_name_plural = "Scan Sessions"

    def __str__(self) -> str:
        if self.name:
            return f"{self.name} ({self.status})"
        return f"Scan {self.created_at.strftime('%Y-%m-%d %H:%M')} ({self.status})"

    @property
    def success_rate(self) -> float:
        """Calculate success rate as percentage."""
        if self.total_files_found == 0:
            return 0.0
        return (self.total_files_processed / self.total_files_found) * 100


class MusicFile(BaseModel):
    """Represents a scanned music file with extracted metadata."""

    scan_session = models.ForeignKey(
        ScanSession,
        on_delete=models.CASCADE,
        related_name="music_files",
    )
    file_path = models.CharField(max_length=1024, help_text="Full path to the file")
    filename = models.CharField(max_length=512, help_text="Filename without path")

    # Metadata fields
    title = models.CharField(max_length=512, blank=True, db_index=True)
    artist = models.CharField(max_length=512, blank=True, db_index=True)
    album = models.CharField(max_length=512, blank=True, db_index=True)
    isrc = models.CharField(max_length=20, blank=True, verbose_name="ISRC")
    genre = models.CharField(max_length=255, blank=True)
    year = models.CharField(max_length=10, blank=True)
    duration = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        help_text="Duration in seconds",
    )

    # Status
    processed = models.BooleanField(default=True)
    error_message = models.TextField(blank=True)

    class Meta:
        ordering = ["artist", "album", "title"]
        verbose_name = "Music File"
        verbose_name_plural = "Music Files"
        indexes = [
            models.Index(fields=["scan_session", "artist", "album"]),
            models.Index(fields=["title", "artist"]),
        ]

    def __str__(self) -> str:
        if self.title and self.artist:
            return f"{self.artist} - {self.title}"
        return self.filename

    @property
    def duration_formatted(self) -> str:
        """Return duration formatted as MM:SS."""
        if self.duration == 0:
            return "--:--"
        minutes = self.duration // 60
        seconds = self.duration % 60
        return f"{minutes}:{seconds:02d}"

    @property
    def has_metadata(self) -> bool:
        """Check if file has meaningful metadata."""
        return bool(self.title or self.artist or self.album)
