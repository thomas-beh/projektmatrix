from django import forms

from .models import Project


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project

        fields = [
            "project_number",
            "title",
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