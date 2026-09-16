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

    def clean_duration_minutes(self):
        minutes = self.cleaned_data["duration_minutes"]
        return minutes

    def save(self, commit=True):
        session = super().save(commit=False)

        # Convert entered minutes into a Python timedelta
        from datetime import timedelta

        session.duration_minutes = timedelta(
            minutes=self.cleaned_data["duration_minutes"]
        )

        if commit:
            session.save()
            self.save_m2m()

        return session

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # When editing an existing session, show the duration as minutes
        if self.instance and self.instance.pk:
            if self.instance.duration_minutes:
                self.initial["duration_minutes"] = int(
                    self.instance.duration_minutes.total_seconds() // 60
                )