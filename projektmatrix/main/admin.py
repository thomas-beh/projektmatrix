from django.contrib import admin

from .models import DevelopmentStage, Project, ProjectStage


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "project_number",
        "title",
        "project_manager",
        "status",
        "planned_start",
        "planned_end",
    )

    search_fields = (
        "project_number",
        "title",
        "project_manager",
        "project_group",
    )

    list_filter = (
        "status",
    )


@admin.register(DevelopmentStage)
class DevelopmentStageAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "name",
        "is_ce_ivd_only",
        "is_active",
    )

    ordering = ("order",)


@admin.register(ProjectStage)
class ProjectStageAdmin(admin.ModelAdmin):
    list_display = (
        "project",
        "stage",
        "status",
        "planned_hours",
        "actual_hours",
        "planned_material_cost",
        "actual_material_cost",
    )

    list_filter = (
        "status",
        "stage",
    )