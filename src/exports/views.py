from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import FileResponse, Http404
from django.conf import settings
from django.utils import timezone
import os
import mimetypes

from playlists.models import Playlist
from .models import ExportJob
from .services import export_playlist


def export_list(request):
    """List all export jobs."""
    exports = ExportJob.objects.select_related("playlist").all()
    return render(request, "exports/export_list.html", {"exports": exports})


def export_create(request, playlist_pk):
    """Create a new export job for a playlist."""
    playlist = get_object_or_404(Playlist, pk=playlist_pk)

    if request.method == "POST":
        format_type = request.POST.get("format_type", "csv")

        if format_type not in [fmt[0] for fmt in ExportJob.FORMAT_CHOICES]:
            messages.error(request, "Invalid export format selected.")
            return redirect("playlists:playlist_detail", pk=playlist_pk)

        # Create export job
        export_job = ExportJob.objects.create(
            playlist=playlist,
            format_type=format_type,
            status="pending",
        )

        # Process export immediately (in production, this would be a celery task)
        try:
            export_job.status = "processing"
            export_job.started_at = timezone.now()
            export_job.save()

            # Ensure export directory exists
            export_dir = os.path.join(settings.MEDIA_ROOT, "exports")
            os.makedirs(export_dir, exist_ok=True)

            # Perform export
            file_path = export_playlist(playlist, format_type, export_dir)
            export_job.file_path = file_path
            export_job.status = "completed"
            export_job.completed_at = timezone.now()
            export_job.save()

            messages.success(
                request,
                f"Playlist exported successfully as {format_type.upper()}."
            )
            return redirect("exports:export_download", pk=export_job.pk)

        except Exception as e:
            export_job.status = "failed"
            export_job.error_message = str(e)
            export_job.completed_at = timezone.now()
            export_job.save()
            messages.error(request, f"Export failed: {e}")
            return redirect("playlists:playlist_detail", pk=playlist_pk)

    # GET request - show export options
    return render(request, "exports/export_create.html", {"playlist": playlist})


def export_download(request, pk):
    """Download an exported file."""
    export_job = get_object_or_404(ExportJob, pk=pk)

    if export_job.status != "completed" or not export_job.file_path:
        messages.error(request, "Export file not available.")
        return redirect("exports:export_list")

    if not os.path.exists(export_job.file_path):
        messages.error(request, "Export file not found.")
        return redirect("exports:export_list")

    # Guess content type
    content_type, _ = mimetypes.guess_type(export_job.file_path)
    if not content_type:
        content_type = "application/octet-stream"

    # Create response with appropriate filename
    response = FileResponse(
        open(export_job.file_path, "rb"),
        content_type=content_type,
        as_attachment=True,
        filename=export_job.filename,
    )

    return response


def export_delete(request, pk):
    """Delete an export job and its file."""
    export_job = get_object_or_404(ExportJob, pk=pk)

    # Delete the file if it exists
    if export_job.file_path and os.path.exists(export_job.file_path):
        try:
            os.remove(export_job.file_path)
        except OSError:
            pass

    playlist_pk = export_job.playlist.pk
    export_job.delete()

    messages.success(request, "Export deleted successfully.")
    return redirect("playlists:playlist_detail", pk=playlist_pk)
