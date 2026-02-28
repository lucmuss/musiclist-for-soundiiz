from django.contrib import admin

from .models import Playlist, PlaylistItem


class PlaylistItemInline(admin.TabularInline):
    model = PlaylistItem
    extra = 0
    fields = ["music_file", "position"]
    autocomplete_fields = ["music_file"]


@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ["name", "total_tracks", "duration_formatted", "created_at"]
    search_fields = ["name", "description"]
    readonly_fields = ["total_tracks", "duration_formatted", "created_at", "updated_at"]
    inlines = [PlaylistItemInline]
    date_hierarchy = "created_at"


@admin.register(PlaylistItem)
class PlaylistItemAdmin(admin.ModelAdmin):
    list_display = ["__str__", "playlist", "music_file", "position"]
    list_filter = ["playlist", "created_at"]
    search_fields = ["playlist__name", "music_file__title", "music_file__artist"]
    autocomplete_fields = ["playlist", "music_file"]
