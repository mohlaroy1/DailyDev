from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum, Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .forms import CodingSessionForm
from .models import CodingSession, Technology


@login_required
def session_list(request):

    query = request.GET.get("q", "")

    sessions = (
        CodingSession.objects
        .select_related("user")
        .prefetch_related("technologies")
        .filter(user=request.user)
        .order_by("-date", "-created_at")
    )

    if query:
        sessions = sessions.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(technologies__name__icontains=query)
        ).distinct()

    paginator = Paginator(sessions, 5)

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "tracker/session_list.html",
        {
            "sessions": page_obj,
            "page_obj": page_obj,
            "query": query,
        },
    )


@login_required
def session_create(request):
    if request.method == "POST":
        form = CodingSessionForm(request.POST)

        if form.is_valid():
            session = form.save(commit=False)

            session.user = request.user

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


@login_required
def session_detail(request, session_id):
    session = get_object_or_404(
        CodingSession,
        id=session_id,
        user=request.user,
    )

    return render(
        request,
        "tracker/session_detail.html",
        {"session": session},
    )


@login_required
def session_edit(request, session_id):
    session = get_object_or_404(
        CodingSession,
        id=session_id,
        user=request.user,
    )

    if request.method == "POST":
        session.title = request.POST.get("title")
        session.description = request.POST.get("description")
        session.duration_minutes = request.POST.get("duration_minutes")

        session.save()

        return redirect(
            "session_detail",
            session_id=session.id,
        )

    return render(
        request,
        "tracker/session_edit.html",
        {"session": session},
    )


@login_required
def session_delete(request, session_id):
    session = get_object_or_404(
        CodingSession,
        id=session_id,
        user=request.user,
    )

    if request.method == "POST":
        session.delete()
        return redirect("session_list")

    return render(
        request,
        "tracker/session_confirm_delete.html",
        {"session": session},
    )


@login_required
def dashboard(request):
    user_sessions = CodingSession.objects.filter(user=request.user)

    total_sessions = user_sessions.count()

    total_minutes = user_sessions.aggregate(
        total=Sum("duration_minutes")
    )["total"] or 0

    total_technologies = Technology.objects.count()

    latest_session = user_sessions.order_by("-date").first()

    context = {
        "total_sessions": total_sessions,
        "total_minutes": total_minutes,
        "total_technologies": total_technologies,
        "latest_session": latest_session,
    }

    return render(
        request,
        "tracker/dashboard.html",
        context,
    )