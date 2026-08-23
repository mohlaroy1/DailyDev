from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CodingSessionForm
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


def session_create(request):
    if request.method == "POST":
        form = CodingSessionForm(request.POST)

        if form.is_valid():
            session = form.save(commit=False)

            # Temporary solution until authentication is added
            session.user = get_object_or_404(User, username="YOUR_USERNAME")

            session.save()

            form.save_m2m()

            return redirect("session_list")

    else:
        form = CodingSessionForm()

    return render(
        request,
        "tracker/session_form.html",
        {"form": form},
    )
