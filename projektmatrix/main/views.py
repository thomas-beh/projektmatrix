from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .models import Projekt


class ProjektListeView(ListView):
    model = Projekt
    template_name = "main/projekt_liste.html"
    context_object_name = "projekte"
    paginate_by = 10


class ProjektDetailView(DetailView):
    model = Projekt
    template_name = "main/projekt_detail.html"
    context_object_name = "projekt"


class ProjektErstellenView(CreateView):
    model = Projekt
    template_name = "main/projekt_formular.html"
    fields = [
        "projektnummer",
        "titel",
        "status",
        "startdatum",
        "enddatum",
    ]


class ProjektBearbeitenView(UpdateView):
    model = Projekt
    template_name = "main/projekt_formular.html"
    fields = [
        "projektnummer",
        "titel",
        "status",
        "startdatum",
        "enddatum",
    ]


class ProjektLoeschenView(DeleteView):
    model = Projekt
    template_name = "main/projekt_loeschen.html"
    success_url = reverse_lazy("projekt-liste")