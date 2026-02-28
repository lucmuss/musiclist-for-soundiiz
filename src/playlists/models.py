from django.db import models
from core.models import BaseModel
from scanner.models import MusicFile


class Playlist(BaseModel):
    """Represents a playlist of music files."""

    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Playlist"
        verbose_name_plural = "Playlists"

    def __str__(self) -> str:
        return self.name

    @property
    def total_tracks(self) -> int:
        """Return total number of tracks in playlist."""
        return self.items.count()

    @property
    def total_duration(self) -> int:
        """Return total duration in seconds."""
        return sum(item.music_file.duration for item in self.items.all())

    @property
    def duration_formatted(self) -> str:
        """Return total duration formatted as H:MM:SS."""
        total_seconds = self.total_duration
        if total_seconds == 0:
            return "0:00"
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        if hours > 0:
            return f"{hours}:{minutes:02d}:{seconds:02d}"
        return f"{minutes}:{seconds:02d}"


class PlaylistItem(BaseModel):
    """Represents a music file in a playlist."""

    playlist = models.ForeignKey(
        Playlist,
        on_delete=models.CASCADE,
        related_name="items",
    )
    music_file = models.ForeignKey(
        MusicFile,
        on_delete=models.CASCADE,
        related_name="playlist_items",
    )
    position = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["position", "created_at"]
        verbose_name = "Playlist Item"
        verbose_name_plural = "Playlist Items"
        unique_together = [["playlist", "music_file"]]

    def __str__(self) -> str:
        return f"{self.position + 1}. {self.music_file}"

    def save(self, *args, **kwargs):
        """Auto-assign position if not set."""
        if self.position == 0 and not self.pk:
            last_position = self.playlist.items.count()
            self.position = last_position
        super().save(*args, **kwargs)
