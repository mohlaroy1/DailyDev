from django.shortcuts import render
from .models import CodingSession


def session_list(request):
    sessions = (
        CodingSession.objects
        .select_related("user")
        .prefetch_related("technologies")
        .order_by("-date", "-created_at")
    )

    return render(
        request,
        "tracker/session_list.html",
        {"sessions": sessions},
    )
