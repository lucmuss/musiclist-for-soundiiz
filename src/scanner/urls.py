from django.urls import path
from . import views

app_name = "scanner"

urlpatterns = [
    path("", views.scan_list, name="scan_list"),
    path("upload/", views.scan_upload, name="scan_upload"),
    path("<uuid:pk>/", views.scan_detail, name="scan_detail"),
    path("<uuid:pk>/delete/", views.scan_delete, name="scan_delete"),
    path("files/<uuid:pk>/", views.music_file_detail, name="music_file_detail"),
]
