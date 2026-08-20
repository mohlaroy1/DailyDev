from django.db import models
from django.contrib.auth.models import User

class Technology(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class CodingSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="coding_sessions",)

    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    duration_minutes = models.DurationField()
    technologies = models.ManyToManyField(Technology, related_name="sessions", blank=True,)
    github_commit = models.CharField(max_length=100, blank=True,)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.date}"

