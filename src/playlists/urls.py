from django.urls import path
from . import views

app_name = "playlists"

urlpatterns = [
    path("", views.playlist_list, name="playlist_list"),
    path("create/", views.playlist_create, name="playlist_create"),
    path("<uuid:pk>/", views.playlist_detail, name="playlist_detail"),
    path("<uuid:pk>/edit/", views.playlist_edit, name="playlist_edit"),
    path("<uuid:pk>/delete/", views.playlist_delete, name="playlist_delete"),
    path("<uuid:pk>/add-tracks/", views.playlist_add_tracks, name="playlist_add_tracks"),
    path("<uuid:playlist_pk>/remove-track/<uuid:item_pk>/", views.playlist_remove_track, name="playlist_remove_track"),
    path("<uuid:pk>/reorder/", views.playlist_reorder, name="playlist_reorder"),
]
