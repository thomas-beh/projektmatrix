from django.db import models
from django.urls import reverse #für Weiterleitungen nach Speichern/Bearbeiten


# Create your models here.
class Projekt(models.Model):
    STATUS_AUSWAHL = [
        ("idee", "Projektidee"),
        ("aktiv", "Aktiv"),
        ("pausiert", "Pausiert"),
        ("abgeschlossen", "Abgeschlossen"),
        ("verzug", "in Verzug"),
        ("problem", "Problem")
    ]

    titel = models.CharField(
        max_length=200,
        verbose_name="Projekttitel",
    )
    projektnummer = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Projektnummer",
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_AUSWAHL,
        default="idee",
    )
    startdatum = models.DateField(
        null=True,
        blank=True,
        verbose_name="Projektbeginn",
    )
    enddatum = models.DateField(
        null=True,
        blank=True,
        verbose_name="vorauss. Projektende",
    )
    class Meta:
        ordering = ["titel"]
        verbose_name = "Projekt"
        verbose_name_plural = "Projekte"

    def __str__(self):
        return f"{self.projektnummer} – {self.titel}"

    def get_absolute_url(self):
        return reverse(
            "projekt-detail",
            kwargs={"pk": self.pk},
        )

