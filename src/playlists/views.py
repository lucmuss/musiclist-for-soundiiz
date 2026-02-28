from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from scanner.models import MusicFile

from .models import Playlist, PlaylistItem


def playlist_list(request):
    """List all playlists."""
    playlists = Playlist.objects.all()
    paginator = Paginator(playlists, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "playlists/playlist_list.html", {"page_obj": page_obj})


def playlist_detail(request, pk):
    """View details of a playlist."""
    playlist = get_object_or_404(Playlist, pk=pk)
    items = playlist.items.select_related("music_file").all()
    paginator = Paginator(items, 25)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        "playlists/playlist_detail.html",
        {
            "playlist": playlist,
            "page_obj": page_obj,
        },
    )


def playlist_create(request):
    """Create a new playlist."""
    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        description = request.POST.get("description", "").strip()

        if not name:
            messages.error(request, "Please provide a playlist name.")
            return render(request, "playlists/playlist_form.html")

        playlist = Playlist.objects.create(name=name, description=description)
        messages.success(request, f"Playlist '{name}' created successfully.")
        return redirect("playlists:playlist_detail", pk=playlist.pk)

    return render(request, "playlists/playlist_form.html")


def playlist_edit(request, pk):
    """Edit an existing playlist."""
    playlist = get_object_or_404(Playlist, pk=pk)

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        description = request.POST.get("description", "").strip()

        if not name:
            messages.error(request, "Please provide a playlist name.")
            return render(request, "playlists/playlist_form.html", {"playlist": playlist})

        playlist.name = name
        playlist.description = description
        playlist.save()
        messages.success(request, f"Playlist '{name}' updated successfully.")
        return redirect("playlists:playlist_detail", pk=playlist.pk)

    return render(request, "playlists/playlist_form.html", {"playlist": playlist})


@require_POST
def playlist_delete(request, pk):
    """Delete a playlist."""
    playlist = get_object_or_404(Playlist, pk=pk)
    name = playlist.name
    playlist.delete()
    messages.success(request, f"Playlist '{name}' deleted successfully.")
    return redirect("playlists:playlist_list")


def playlist_add_tracks(request, pk):
    """Add tracks to a playlist."""
    playlist = get_object_or_404(Playlist, pk=pk)

    if request.method == "POST":
        music_file_ids = request.POST.getlist("music_files")

        if not music_file_ids:
            messages.error(request, "Please select at least one track.")
            return redirect("playlists:playlist_add_tracks", pk=playlist.pk)

        added_count = 0
        for music_file_id in music_file_ids:
            try:
                music_file = MusicFile.objects.get(pk=music_file_id)
                PlaylistItem.objects.get_or_create(
                    playlist=playlist,
                    music_file=music_file,
                )
                added_count += 1
            except MusicFile.DoesNotExist:
                continue

        messages.success(request, f"Added {added_count} track(s) to playlist.")
        return redirect("playlists:playlist_detail", pk=playlist.pk)

    # Get search query
    search_query = request.GET.get("q", "").strip()
    scan_session = request.GET.get("scan_session", "").strip()

    # Filter music files
    music_files = MusicFile.objects.filter(processed=True)

    if search_query:
        music_files = music_files.filter(
            Q(title__icontains=search_query)
            | Q(artist__icontains=search_query)
            | Q(album__icontains=search_query)
        )

    if scan_session:
        music_files = music_files.filter(scan_session_id=scan_session)

    # Exclude already in playlist
    existing_ids = playlist.items.values_list("music_file_id", flat=True)
    music_files = music_files.exclude(id__in=existing_ids)

    paginator = Paginator(music_files, 25)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "playlists/playlist_add_tracks.html",
        {
            "playlist": playlist,
            "page_obj": page_obj,
            "search_query": search_query,
        },
    )


@require_POST
def playlist_remove_track(request, playlist_pk, item_pk):
    """Remove a track from a playlist."""
    playlist = get_object_or_404(Playlist, pk=playlist_pk)
    item = get_object_or_404(PlaylistItem, pk=item_pk, playlist=playlist)
    item.delete()

    # Reorder remaining items
    for idx, remaining_item in enumerate(playlist.items.all()):
        remaining_item.position = idx
        remaining_item.save(update_fields=["position"])

    messages.success(request, "Track removed from playlist.")
    return redirect("playlists:playlist_detail", pk=playlist.pk)


@require_POST
def playlist_reorder(request, pk):
    """Reorder tracks in a playlist."""
    playlist = get_object_or_404(Playlist, pk=pk)
    item_order = request.POST.getlist("item_order[]")

    for idx, item_id in enumerate(item_order):
        try:
            item = PlaylistItem.objects.get(pk=item_id, playlist=playlist)
            item.position = idx
            item.save(update_fields=["position"])
        except PlaylistItem.DoesNotExist:
            continue

    messages.success(request, "Playlist reordered successfully.")
    return redirect("playlists:playlist_detail", pk=playlist.pk)
