from django import forms
from .models import CodingSession


class CodingSessionForm(forms.ModelForm):
    class Meta:
        model = CodingSession

        fields = [
            "title",
            "description",
            "date",
            "duration_minutes",
            "technologies",
            "github_commit",
        ]

        widgets = {
            "date": forms.DateInput(
                attrs={
                    "type": "date",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "rows": 5,
                    "placeholder": "What did you work on today?",
                }
            ),
            "title": forms.TextInput(
                attrs={
                    "placeholder": "e.g. Built the session creation feature",
                }
            ),
            "duration_minutes": forms.NumberInput(
                attrs={
                    "min": 1,
                    "placeholder": "Minutes spent coding",
                }
            ),
            "github_commit": forms.TextInput(
                attrs={
                    "placeholder": "Optional commit hash",
                }
            ),
        }