from django.urls import path

from .views import (
    ProjektBearbeitenView,
    ProjektDetailView,
    ProjektErstellenView,
    ProjektListeView,
    ProjektLoeschenView,
)


urlpatterns = [
    path(
        "",
        ProjektListeView.as_view(),
        name="projekt-liste",
    ),
    path(
        "projekte/neu/",
        ProjektErstellenView.as_view(),
        name="projekt-erstellen",
    ),
    path(
        "projekte/<int:pk>/",
        ProjektDetailView.as_view(),
        name="projekt-detail",
    ),
    path(
        "projekte/<int:pk>/bearbeiten/",
        ProjektBearbeitenView.as_view(),
        name="projekt-bearbeiten",
    ),
    path(
        "projekte/<int:pk>/loeschen/",
        ProjektLoeschenView.as_view(),
        name="projekt-loeschen",
    ),
]