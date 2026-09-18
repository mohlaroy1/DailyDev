from django import forms
from .models import CodingSession


class CodingSessionForm(forms.ModelForm):
    duration_minutes = forms.IntegerField(
        min_value=1,
        label="Duration (minutes)",
        widget=forms.NumberInput(
            attrs={
                "min": 1,
                "placeholder": "e.g. 60",
            }
        ),
    )

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
            "github_commit": forms.TextInput(
                attrs={
                    "placeholder": "Optional commit hash",
                }
            ),
        }