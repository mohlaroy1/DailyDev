from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum

from .forms import CodingSessionForm
from .models import CodingSession, Technology


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



def session_delete(request, session_id):
    session = get_object_or_404(CodingSession, id=session_id)

    if request.method == "POST":
        session.delete()
        return redirect("session_list")

    return render(
        request,
        "tracker/session_confirm_delete.html",
        {"session": session}
    )


def dashboard(request):

    total_sessions = CodingSession.objects.count()

    total_minutes = CodingSession.objects.aggregate(
        total=Sum("duration_minutes")
    )["total"] or 0

    total_technologies = Technology.objects.count()

    latest_session = CodingSession.objects.order_by("-date").first()

    context = {
        "total_sessions": total_sessions,
        "total_minutes": total_minutes,
        "total_technologies": total_technologies,
        "latest_session": latest_session,
    }

    return render(
        request,
        "tracker/dashboard.html",
        context
    )