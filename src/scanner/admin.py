from django.contrib import admin

from .models import MusicFile, ScanSession


class MusicFileInline(admin.TabularInline):
    model = MusicFile
    extra = 0
    fields = ["filename", "title", "artist", "album", "duration_formatted", "processed"]
    readonly_fields = ["duration_formatted"]
    can_delete = False
    show_change_link = True
    max_num = 10


@admin.register(ScanSession)
class ScanSessionAdmin(admin.ModelAdmin):
    list_display = [
        "__str__",
        "source_path",
        "status",
        "total_files_found",
        "total_files_processed",
        "success_rate_display",
        "created_at",
    ]
    list_filter = ["status", "recursive", "created_at"]
    search_fields = ["name", "source_path"]
    readonly_fields = [
        "total_files_found",
        "total_files_processed",
        "total_files_failed",
        "success_rate",
        "started_at",
        "completed_at",
        "created_at",
        "updated_at",
    ]
    inlines = [MusicFileInline]
    date_hierarchy = "created_at"

    @admin.display(description="Success Rate")
    def success_rate_display(self, obj: ScanSession) -> str:
        return f"{obj.success_rate:.1f}%"


@admin.register(MusicFile)
class MusicFileAdmin(admin.ModelAdmin):
    list_display = [
        "__str__",
        "artist",
        "album",
        "duration_formatted",
        "scan_session",
        "processed",
    ]
    list_filter = ["processed", "genre", "year", "created_at"]
    search_fields = ["title", "artist", "album", "filename", "isrc"]
    readonly_fields = ["duration_formatted", "created_at", "updated_at"]
    date_hierarchy = "created_at"
