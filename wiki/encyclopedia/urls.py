from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>",views.wiki, name="wiki"),
    path("create",views.create, name="create"),
    path("randome", views.randome, name="random"),
    path("search/", views.search, name = "search"),
    path("edit/<str:title>",views.edit, name="edit")
]
