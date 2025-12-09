from django.urls import path

from . import views

urlpatterns = [
    path("home", views.index, name="index"),
    path("", views.index, name="home"),
    path("about", views.about, name="about"),
    path("privacy", views.privacy, name="privacy"),
    path("analyze", views.analyze, name="analyze"),
    path("results", views.results, name="results"),
]
