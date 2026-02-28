from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
import os

from .models import ScanSession, MusicFile
from .services import MusicFileExtractor


def scan_list(request):
    """List all scan sessions."""
    scans = ScanSession.objects.all()
    paginator = Paginator(scans, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "scanner/scan_list.html", {"page_obj": page_obj})


def scan_detail(request, pk):
    """View details of a scan session."""
    scan = get_object_or_404(ScanSession, pk=pk)
    music_files = scan.music_files.all()
    paginator = Paginator(music_files, 25)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "scanner/scan_detail.html", {
        "scan": scan,
        "page_obj": page_obj,
    })


def scan_upload(request):
    """Handle upload and scanning of music files."""
    if request.method == "POST":
        directory_path = request.POST.get("directory_path", "").strip()
        recursive = request.POST.get("recursive", "on") == "on"
        session_name = request.POST.get("session_name", "").strip()

        if not directory_path:
            messages.error(request, "Please provide a directory path.")
            return render(request, "scanner/scan_upload.html")

        if not os.path.isdir(directory_path):
            messages.error(request, f"Directory not found: {directory_path}")
            return render(request, "scanner/scan_upload.html")

        # Create scan session
        scan_session = ScanSession.objects.create(
            name=session_name or None,
            source_path=directory_path,
            recursive=recursive,
            status="scanning",
            started_at=timezone.now(),
        )

        try:
            # Perform scan
            extractor = MusicFileExtractor()
            music_files = extractor.find_music_files(directory_path, recursive)
            scan_session.total_files_found = len(music_files)
            scan_session.save()

            # Extract metadata for each file
            for file_path in music_files:
                try:
                    metadata = extractor.extract_metadata(file_path)
                    MusicFile.objects.create(
                        scan_session=scan_session,
                        file_path=metadata["file_path"],
                        filename=metadata["filename"],
                        title=metadata["title"],
                        artist=metadata["artist"],
                        album=metadata["album"],
                        isrc=metadata["isrc"],
                        genre=metadata["genre"],
                        year=metadata["year"],
                        duration=metadata["duration"],
                        processed=True,
                    )
                    scan_session.total_files_processed += 1
                except Exception as e:
                    MusicFile.objects.create(
                        scan_session=scan_session,
                        file_path=str(file_path),
                        filename=file_path.name,
                        processed=False,
                        error_message=str(e),
                    )
                    scan_session.total_files_failed += 1

            # Update session status
            scan_session.status = "completed"
            scan_session.completed_at = timezone.now()
            scan_session.save()

            messages.success(
                request,
                f"Scan completed! Found {scan_session.total_files_found} files, "
                f"processed {scan_session.total_files_processed} successfully."
            )
            return redirect("scanner:scan_detail", pk=scan_session.pk)

        except Exception as e:
            scan_session.status = "failed"
            scan_session.error_message = str(e)
            scan_session.completed_at = timezone.now()
            scan_session.save()
            messages.error(request, f"Scan failed: {e}")
            return redirect("scanner:scan_list")

    return render(request, "scanner/scan_upload.html")


@require_POST
def scan_delete(request, pk):
    """Delete a scan session and all associated music files."""
    scan = get_object_or_404(ScanSession, pk=pk)
    scan.delete()
    messages.success(request, "Scan session deleted successfully.")
    return redirect("scanner:scan_list")


def music_file_detail(request, pk):
    """View details of a single music file."""
    music_file = get_object_or_404(MusicFile, pk=pk)
    return render(request, "scanner/music_file_detail.html", {"music_file": music_file})
