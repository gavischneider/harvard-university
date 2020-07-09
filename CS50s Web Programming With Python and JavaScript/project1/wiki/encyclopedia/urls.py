from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>/", views.entry, name="entry"),
    path("search", views.search, name="search"),
    path("newPage", views.newPage, name="newPage"),
    path("edit/<str:entry>", views.edit, name="edit"),
    path("randomPage", views.randomPage, name="randomPage")
]
