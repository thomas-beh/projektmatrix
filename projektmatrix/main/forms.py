from django import forms

from .models import (
    Project,
    ProjectStage,
    ProjectStageAttachment,
)


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project

        fields = [
            "project_number",
            "title",
            "project_type",
            "project_group",
            "project_manager",
            "status",
            "planned_start",
            "planned_end",
            "actual_start",
            "actual_end",
            "description",
            "has_problem",
            "problem_description",
        ]

        widgets = {
            "project_number": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "title": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "project_type": forms.Select(
                attrs={"class": "form-select"}
            ),
            "project_group": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "project_manager": forms.TextInput(
                attrs={"class": "form-control"}
            ),
            "status": forms.Select(
                attrs={"class": "form-select"}
            ),
            "planned_start": forms.DateInput(
                format="%Y-%m-%d",
                attrs={
                    "type": "date",
                    "class": "form-control",
                },
            ),
            "planned_end": forms.DateInput(
                format="%Y-%m-%d",
                attrs={
                    "type": "date",
                    "class": "form-control",
                },
            ),
            "actual_start": forms.DateInput(
                format="%Y-%m-%d",
                attrs={
                    "type": "date",
                    "class": "form-control",
                },
            ),
            "actual_end": forms.DateInput(
                format="%Y-%m-%d",
                attrs={
                    "type": "date",
                    "class": "form-control",
                },
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                }
            ),
            "has_problem": forms.CheckboxInput(
                attrs={"class": "form-check-input"}
            ),
            "problem_description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                }
            ),
        }

class ProjectStageForm(forms.ModelForm):
    class Meta:
        model = ProjectStage

        fields = [
            "status",
            "responsible_person",
            "planned_hours",
            "actual_hours",
            "planned_material_cost",
            "actual_material_cost",
            "planned_start",
            "planned_end",
            "actual_start",
            "actual_end",
            "notes",
        ]

        widgets = {
            "status": forms.Select(
                attrs={"class": "form-select"}
            ),

            "responsible_person": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "planned_hours": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0",
                    "step": "0.25",
                }
            ),

            "actual_hours": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0",
                    "step": "0.25",
                }
            ),

            "planned_material_cost": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0",
                    "step": "0.01",
                }
            ),

            "actual_material_cost": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "min": "0",
                    "step": "0.01",
                }
            ),

            "planned_start": forms.DateInput(
                format="%Y-%m-%d",
                attrs={
                    "type": "date",
                    "class": "form-control",
                },
            ),

            "planned_end": forms.DateInput(
                format="%Y-%m-%d",
                attrs={
                    "type": "date",
                    "class": "form-control",
                },
            ),

            "actual_start": forms.DateInput(
                format="%Y-%m-%d",
                attrs={
                    "type": "date",
                    "class": "form-control",
                },
            ),

            "actual_end": forms.DateInput(
                format="%Y-%m-%d",
                attrs={
                    "type": "date",
                    "class": "form-control",
                },
            ),

            "notes": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                }
            ),
        }

        #for correct date check
        def clean(self):
            cleaned_data = super().clean()

            planned_start = cleaned_data.get("planned_start")
            planned_end = cleaned_data.get("planned_end")

            actual_start = cleaned_data.get("actual_start")
            actual_end = cleaned_data.get("actual_end")

            if (
                planned_start
                and planned_end
                and planned_end < planned_start
            ):
                self.add_error(
                    "planned_end",
                    "Planned end cannot be before planned start.",
                )

            if (
                actual_start
                and actual_end
                and actual_end < actual_start
            ):
                self.add_error(
                    "actual_end",
                    "Actual end cannot be before actual start.",
                )

            return cleaned_data

class ProjectStageAttachmentForm(forms.ModelForm):
    class Meta:
        model = ProjectStageAttachment

        fields = [
            "file",
            "description",
        ]

        widgets = {
            "file": forms.FileInput(
                attrs={"class": "form-control"}
            ),
            "description": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Optional description",
                }
            ),
        }