from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect

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


def session_detail(request, session_id):
    session = get_object_or_404(CodingSession, id=session_id)
    return render(request, "tracker/session_detail.html", {"session": session},)


def session_edit(request, session_id):
    session = get_object_or_404(CodingSession, id=session_id)

    if request.method == "POST":
        session.title = request.POST.get("title")
        session.description = request.POST.get("description")
        session.duration_minutes = request.POST.get("duration_minutes")

        session.save()

        return redirect("session_detail", session_id=session.id)

    return render(
        request,
        "tracker/session_edit.html",
        {"session": session}
    )


