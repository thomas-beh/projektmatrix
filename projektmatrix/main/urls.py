from django.urls import path

from .views import (
    ProjectCreateView,
    ProjectDeleteView,
    ProjectDetailView,
    ProjectListView,
    ProjectStageUpdateView,
    ProjectUpdateView,
    ProjectStageDetailView,
    project_stage_attachment_upload,
    WorkStepCreateView,
    WorkStepUpdateView,
    WorkStepDeleteView,
)

urlpatterns = [
    path(
        "",
        ProjectListView.as_view(),
        name="project-list",
    ),
    path(
        "projects/new/",
        ProjectCreateView.as_view(),
        name="project-create",
    ),
    path(
        "projects/<int:pk>/",
        ProjectDetailView.as_view(),
        name="project-detail",
    ),
    path(
        "projects/<int:pk>/edit/",
        ProjectUpdateView.as_view(),
        name="project-update",
    ),
    path(
        "projects/<int:pk>/delete/",
        ProjectDeleteView.as_view(),
        name="project-delete",
    ),
    path(
    "project-stages/<int:pk>/edit/",
    ProjectStageUpdateView.as_view(),
    name="project-stage-update",
    ),
    path(
    "project-stages/<int:pk>/",
    ProjectStageDetailView.as_view(),
    name="project-stage-detail",
    ),
    path(
    "project-stages/<int:pk>/attachments/upload/",
    project_stage_attachment_upload,
    name="project-stage-attachment-upload",
    ),
    path(
    "project-stages/<int:stage_pk>/work-steps/new/",
    WorkStepCreateView.as_view(),
    name="work-step-create",
    ),

    path(
        "work-steps/<int:pk>/edit/",
        WorkStepUpdateView.as_view(),
        name="work-step-update",
    ),

    path(
        "work-steps/<int:pk>/delete/",
        WorkStepDeleteView.as_view(),
        name="work-step-delete",
    ),
]