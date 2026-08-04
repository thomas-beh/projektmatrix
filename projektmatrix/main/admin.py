from django.contrib import admin

from .models import Projekt

# Register your models here.
@admin.register(Projekt)
class ProjektAdmin(admin.ModelAdmin):
    list_display = (
        "projektnummer",
        "titel",
        "status",
        "startdatum",
        "enddatum",
    )
    search_fields = (
        "projektnummer",
        "titel",
    )
    list_filter = (
        "status",
    )