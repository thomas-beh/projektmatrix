from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.db import transaction
from django.utils import timezone
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import (
    ProjectForm,
    ProjectStageForm,
    ProjectStageAttachmentForm,
)
from .models import (
    DevelopmentStage,
    Project,
    ProjectStage,
    ProjectStageAttachment,
)
from datetime import timedelta


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        project = self.object

        project_stages = (
            project.project_stages
            .select_related("stage")
            .order_by("stage__order")
        )

        # Project Summary

        total_planned_hours = sum(
            stage.planned_hours or 0
            for stage in project_stages
        )

        total_actual_hours = sum(
            stage.actual_hours or 0
            for stage in project_stages
        )

        total_planned_cost = sum(
            stage.planned_material_cost or 0
            for stage in project_stages
        )

        total_actual_cost = sum(
            stage.actual_material_cost or 0
            for stage in project_stages
        )

        scheduled_stages = [
            stage
            for stage in project_stages
            if stage.planned_start and stage.planned_end
        ]

        if scheduled_stages:
            earliest_planned_start = min(
                stage.planned_start
                for stage in scheduled_stages
            )

            latest_planned_end = max(
                stage.planned_end
                for stage in scheduled_stages
            )

            total_planned_duration = (
                latest_planned_end - earliest_planned_start
            ).days + 1
        else:
            total_planned_duration = None


        actual_stages = [
            stage
            for stage in project_stages
            if stage.actual_start and stage.actual_end
        ]

        if actual_stages:
            earliest_actual_start = min(
                stage.actual_start
                for stage in actual_stages
            )

            latest_actual_end = max(
                stage.actual_end
                for stage in actual_stages
            )

            total_actual_duration = (
                latest_actual_end - earliest_actual_start
            ).days + 1
        else:
            total_actual_duration = None

        context["total_planned_hours"] = total_planned_hours
        context["total_actual_hours"] = total_actual_hours

        context["total_planned_cost"] = total_planned_cost
        context["total_actual_cost"] = total_actual_cost

        context["total_planned_duration"] = total_planned_duration
        context["total_actual_duration"] = total_actual_duration

        scheduled_stages = [
            project_stage
            for project_stage in project_stages
            if project_stage.planned_start
            and project_stage.planned_end
        ]

        if not scheduled_stages:
            context["gantt_available"] = False
            return context

        stage_start = min(
            project_stage.planned_start
            for project_stage in scheduled_stages
        )

        if project.planned_start:
            gantt_start = min(
                project.planned_start,
                stage_start,
            )
        else:
            gantt_start = stage_start

        stage_end = max(
            project_stage.planned_end
            for project_stage in scheduled_stages
        )

        if project.planned_start:
            project_start_offset = (
                project.planned_start - gantt_start
            ).days

            context["project_start_column"] = (
                project_start_offset + 3
            )
        else:
            context["project_start_column"] = 3

        if project.planned_end:
            gantt_end = max(
                project.planned_end,
                stage_end,
            )
        else:
            gantt_end = stage_end

        gantt_total_days = (
            gantt_end - gantt_start
        ).days + 1

        gantt_days = []

        current_date = gantt_start

        while current_date <= gantt_end:
            gantt_days.append(
                {
                    "date": current_date,
                    "weekday": current_date.strftime("%a"),
                    "day": current_date.strftime("%d"),
                    "is_weekend": current_date.weekday() >= 5,
                }
            )

            current_date += timedelta(days=1)

        gantt_rows = []

        for project_stage in project_stages:

            if (
                project_stage.planned_start
                and project_stage.planned_end
            ):
                offset_days = (
                    project_stage.planned_start
                    - gantt_start
                ).days

                duration_days = (
                    project_stage.planned_end
                    - project_stage.planned_start
                ).days + 1

                gantt_rows.append(
                    {
                        "project_stage": project_stage,
                        "has_schedule": True,
                        "start_column": offset_days + 3,
                        "duration_days": duration_days,
                    }
                )

            else:
                gantt_rows.append(
                    {
                        "project_stage": project_stage,
                        "has_schedule": False,
                    }
                )

        context["gantt_available"] = True
        context["gantt_start"] = gantt_start
        context["gantt_end"] = gantt_end
        context["gantt_total_days"] = gantt_total_days
        context["gantt_days"] = gantt_days
        context["gantt_rows"] = gantt_rows

        return context

class ProjectCreateView(CreateView):
    model = Project
    form_class = ProjectForm
    template_name = "main/project_form.html"

    @transaction.atomic
    def form_valid(self, form):
        response = super().form_valid(form)

        stages = DevelopmentStage.objects.filter(
            is_active=True
        )

        if self.object.project_type == "general":
            stages = stages.exclude(
                code="post-market-surveillance"
            )

        project_stages = [
            ProjectStage(
                project=self.object,
                stage=stage,
            )
            for stage in stages
        ]

        ProjectStage.objects.bulk_create(
            project_stages,
            ignore_conflicts=True,
        )

        return response


class ProjectUpdateView(UpdateView):
    model = Project
    form_class = ProjectForm
    template_name = "main/project_form.html"


class ProjectDeleteView(DeleteView):
    model = Project
    template_name = "main/project_delete.html"
    success_url = reverse_lazy("project-list")

class ProjectStageUpdateView(UpdateView):
    model = ProjectStage
    form_class = ProjectStageForm
    template_name = "main/project_stage_form.html"
    context_object_name = "project_stage"

    def get_success_url(self):
        return reverse_lazy(
            "project-detail",
            kwargs={"pk": self.object.project.pk},
        )

class ProjectStageDetailView(DetailView):
    model = ProjectStage
    template_name = "main/project_stage_detail.html"
    context_object_name = "project_stage"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["attachment_form"] = (
            ProjectStageAttachmentForm()
        )

        return context

def project_stage_attachment_upload(request, pk):
    project_stage = get_object_or_404(
        ProjectStage,
        pk=pk,
    )

    if request.method == "POST":
        form = ProjectStageAttachmentForm(
            request.POST,
            request.FILES,
        )

        if form.is_valid():
            attachment = form.save(commit=False)
            attachment.project_stage = project_stage
            attachment.save()

    return redirect(
        "project-stage-detail",
        pk=project_stage.pk,
    )