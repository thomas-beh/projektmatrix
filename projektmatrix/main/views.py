from django.db.models import Q
from django.utils import timezone
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import ProjectForm
from .models import Project


class ProjectListView(ListView):
    model = Project
    template_name = "main/project_list.html"
    context_object_name = "projects"
    paginate_by = 10

    allowed_sort_fields = {
        "project_number": "project_number",
        "-project_number": "-project_number",
        "title": "title",
        "-title": "-title",
        "status": "status",
        "-status": "-status",
        "planned_start": "planned_start",
        "-planned_start": "-planned_start",
        "planned_end": "planned_end",
        "-planned_end": "-planned_end",
    }

    def get_queryset(self):
        queryset = super().get_queryset()

        search_query = self.request.GET.get("q", "").strip()
        status_filter = self.request.GET.get("status", "").strip()
        health_filter = self.request.GET.get("health", "").strip()
        sort_value = self.request.GET.get("sort", "title")
        page_size = self.request.GET.get("page_size", "10")

        if search_query:
            queryset = queryset.filter(
                Q(project_number__icontains=search_query)
                | Q(title__icontains=search_query)
                | Q(project_group__icontains=search_query)
                | Q(project_manager__icontains=search_query)
            )

        if status_filter:
            queryset = queryset.filter(status=status_filter)

        if health_filter == "problem":
            queryset = queryset.filter(has_problem=True)

        elif health_filter == "behind":
            queryset = queryset.filter(
                has_problem=False,
                planned_end__lt=timezone.localdate(),
            ).exclude(status="completed")

        elif health_filter == "completed":
            queryset = queryset.filter(status="completed")

        elif health_filter == "on_track":
            queryset = queryset.filter(
                has_problem=False,
            ).exclude(
                planned_end__lt=timezone.localdate(),
            ).exclude(
                status="completed",
            )

        ordering = self.allowed_sort_fields.get(
            sort_value,
            "title",
        )

        return queryset.order_by(ordering)

    def get_paginate_by(self, queryset):
        requested_size = self.request.GET.get("page_size", "10")

        allowed_sizes = {"10", "20", "50"}

        if requested_size not in allowed_sizes:
            requested_size = "10"

        return int(requested_size)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        query_parameters = self.request.GET.copy()
        query_parameters.pop("page", None)

        context["query_parameters"] = query_parameters.urlencode()
        context["status_choices"] = Project.STATUS_CHOICES
        context["current_search"] = self.request.GET.get("q", "")
        context["current_status"] = self.request.GET.get("status", "")
        context["current_health"] = self.request.GET.get("health", "")
        context["current_sort"] = self.request.GET.get("sort", "title")
        context["current_page_size"] = self.request.GET.get(
            "page_size",
            "10",
        )

        return context


class ProjectDetailView(DetailView):
    model = Project
    template_name = "main/project_detail.html"
    context_object_name = "project"


class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "main/project_form.html"


class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "main/project_form.html"


class ProjectDeleteView(DeleteView):
    model = Project
    template_name = "main/project_delete.html"
    success_url = reverse_lazy("project-list")