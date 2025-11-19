from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about", views.about, name="about"),
    path("privacy", views.privacy, name="privacy"),
    path("results", views.results, name="results"),
]