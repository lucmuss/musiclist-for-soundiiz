from django.urls import path
from . import views

app_name = "exports"

urlpatterns = [
    path("", views.export_list, name="export_list"),
    path("create/<uuid:playlist_pk>/", views.export_create, name="export_create"),
    path("<uuid:pk>/download/", views.export_download, name="export_download"),
    path("<uuid:pk>/delete/", views.export_delete, name="export_delete"),
]
