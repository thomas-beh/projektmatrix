from django.db import models
from django.urls import reverse
from django.utils import timezone


class Project(models.Model):
    PROJECT_TYPE_CHOICES = [
        ("general", "General Development Project"),
        ("ivd", "IVD Kit"),
    ]

    project_type = models.CharField(
        max_length=20,
        choices=PROJECT_TYPE_CHOICES,
        default="general",
        verbose_name="Project Type",
    )

    STATUS_CHOICES = [
        ("idea", "Project Idea"),
        ("active", "Active"),
        ("paused", "Paused"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    project_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Project Number",
    )

    title = models.CharField(
        max_length=200,
        verbose_name="Project Title",
    )

    project_group = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Project Group",
    )

    project_manager = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Project Manager",
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="idea",
    )

    planned_start = models.DateField(
        null=True,
        blank=True,
        verbose_name="Planned Start",
    )

    planned_end = models.DateField(
        null=True,
        blank=True,
        verbose_name="Planned End",
    )

    actual_start = models.DateField(
        null=True,
        blank=True,
        verbose_name="Actual Start",
    )

    actual_end = models.DateField(
        null=True,
        blank=True,
        verbose_name="Actual End",
    )

    description = models.TextField(
        blank=True,
        verbose_name="Description",
    )

    has_problem = models.BooleanField(
        default=False,
        verbose_name="Problem Reported",
    )

    problem_description = models.TextField(
        blank=True,
        verbose_name="Problem Description",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return f"{self.project_number} – {self.title}"

    def get_absolute_url(self):
        return reverse(
            "project-detail",
            kwargs={"pk": self.pk},
        )

    @property
    def is_overdue(self):
        return (
            self.planned_end is not None
            and self.planned_end < timezone.localdate()
            and self.status != "completed"
        )

    @property
    def health_status(self):
        if self.has_problem:
            return "problem"

        if self.is_overdue:
            return "behind"

        if self.status == "completed":
            return "completed"

        return "on_track"

    @property
    def health_label(self):
        labels = {
            "problem": "Problem",
            "behind": "Behind Schedule",
            "completed": "Completed",
            "on_track": "On Track",
        }

        return labels[self.health_status]

#Model for the development stages
class DevelopmentStage(models.Model):
    code = models.SlugField(
        max_length=60,
        unique=True,
    )

    name = models.CharField(
        max_length=200,
        unique=True,
        verbose_name="Stage Name",
    )

    short_name = models.CharField(
        max_length=80,
        blank=True,
        verbose_name="Short Name",
    )

    description = models.TextField(
        blank=True,
    )

    order = models.PositiveIntegerField(
        default=0,
    )

    is_ce_ivd_only = models.BooleanField(
        default=False,
        verbose_name="CE-IVD Only",
    )

    is_active = models.BooleanField(
        default=True,
    )

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.name

#model for connection form fields
class ProjectStage(models.Model):
    STAGE_STATUS_CHOICES = [
        ("not_started", "Not Started"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("blocked", "Blocked"),
        ("not_applicable", "Not Applicable"),
    ]

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="project_stages",
    )

    stage = models.ForeignKey(
        DevelopmentStage,
        on_delete=models.PROTECT,
        related_name="project_entries",
    )

    status = models.CharField(
        max_length=20,
        choices=STAGE_STATUS_CHOICES,
        default="not_started",
    )

    responsible_person = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Responsible Person",
    )

    planned_hours = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Planned Hours",
    )

    actual_hours = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Actual Hours",
    )

    planned_material_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Planned Material Cost",
    )

    actual_material_cost = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Actual Material Cost",
    )

    planned_start = models.DateField(
        null=True,
        blank=True,
        verbose_name="Planned Start",
    )

    planned_end = models.DateField(
        null=True,
        blank=True,
        verbose_name="Planned End",
    )

    actual_start = models.DateField(
        null=True,
        blank=True,
        verbose_name="Actual Start",
    )

    actual_end = models.DateField(
        null=True,
        blank=True,
        verbose_name="Actual End",
    )

    notes = models.TextField(
        blank=True,
    )

    @property
    def planned_duration_days(self):
        if self.planned_start and self.planned_end:
            return (self.planned_end - self.planned_start).days + 1

        return None

    @property
    def actual_duration_days(self):
        if self.actual_start and self.actual_end:
            return (self.actual_end - self.actual_start).days + 1

        return None

    def __str__(self):
        return f"{self.project} – {self.stage}"

    class Meta:
        ordering = ["stage__order"]
        constraints = [
            models.UniqueConstraint(
                fields=["project", "stage"],
                name="unique_project_stage",
            )
        ]

    def __str__(self):
        return f"{self.project} – {self.stage}"

from django.core.validators import FileExtensionValidator


class ProjectStageAttachment(models.Model):
    project_stage = models.ForeignKey(
        ProjectStage,
        on_delete=models.CASCADE,
        related_name="attachments",
    )

    file = models.FileField(
        upload_to="project_stage_attachments/",
        validators=[
            FileExtensionValidator(
                allowed_extensions=[
                    "pdf",
                    "doc",
                    "docx",
                    "xls",
                    "xlsx",
                    "png",
                    "jpg",
                    "jpeg",
                ]
            )
        ],
    )

    description = models.CharField(
        max_length=255,
        blank=True,
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.file.name

class WorkStep(models.Model):
    project_stage = models.ForeignKey(
        ProjectStage,
        on_delete=models.CASCADE,
        related_name="work_steps",
    )

    title = models.CharField(
        max_length=200,
        verbose_name="Work Step",
    )

    order = models.PositiveIntegerField(
        default=0,
    )

    planned_start = models.DateField(
        null=True,
        blank=True,
        verbose_name="Planned Start",
    )

    planned_end = models.DateField(
        null=True,
        blank=True,
        verbose_name="Planned End",
    )

    actual_start = models.DateField(
        null=True,
        blank=True,
        verbose_name="Actual Start",
    )

    actual_end = models.DateField(
        null=True,
        blank=True,
        verbose_name="Actual End",
    )

    notes = models.TextField(
        blank=True,
    )

    class Meta:
        ordering = [
            "order",
            "id",
        ]

    def __str__(self):
        return (
            f"{self.project_stage.stage.name} – "
            f"{self.title}"
        )

    @property
    def planned_duration_days(self):
        if self.planned_start and self.planned_end:
            return (
                self.planned_end
                - self.planned_start
            ).days + 1

        return None

    @property
    def actual_duration_days(self):
        if self.actual_start and self.actual_end:
            return (
                self.actual_end
                - self.actual_start
            ).days + 1

        return None