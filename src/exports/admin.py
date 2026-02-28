from django.contrib import admin
from .models import ExportJob


@admin.register(ExportJob)
class ExportJobAdmin(admin.ModelAdmin):
    list_display = [
        "__str__",
        "format_type",
        "status",
        "created_at",
        "started_at",
        "completed_at",
    ]
    list_filter = ["format_type", "status", "created_at"]
    search_fields = ["playlist__name", "error_message"]
    readonly_fields = [
        "status",
        "file_path",
        "error_message",
        "started_at",
        "completed_at",
        "created_at",
        "updated_at",
    ]
    date_hierarchy = "created_at"
