from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum, Q
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from datetime import timedelta
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta

from .forms import CodingSessionForm
from .models import CodingSession, Technology


@login_required
def session_list(request):
    sessions = (
        CodingSession.objects
        .filter(user=request.user)
        .prefetch_related("technologies")
    )

    # Search
    query = request.GET.get("q", "").strip()

    if query:
        sessions = sessions.filter(
            Q(title__icontains=query)
            | Q(description__icontains=query)
            | Q(technologies__name__icontains=query)
        ).distinct()

    # Technology filter
    technology_id = request.GET.get("technology", "").strip()

    if technology_id:
        sessions = sessions.filter(
            technologies__id=technology_id
        )

    # Date filters
    date_from = request.GET.get("date_from", "").strip()
    date_to = request.GET.get("date_to", "").strip()

    if date_from:
        sessions = sessions.filter(date__gte=date_from)

    if date_to:
        sessions = sessions.filter(date__lte=date_to)

    # Minimum duration
    min_duration = request.GET.get(
        "min_duration",
        "",
    ).strip()

    if min_duration:
        try:
            min_duration_value = int(min_duration)

            if min_duration_value >= 0:
                sessions = sessions.filter(
                    duration_minutes__gte=min_duration_value
                )

        except ValueError:
            pass

    # Sorting
    sort = request.GET.get("sort", "newest")

    if sort == "oldest":
        sessions = sessions.order_by(
            "date",
            "created_at",
        )

    elif sort == "longest":
        sessions = sessions.order_by(
            "-duration_minutes",
            "-date",
        )

    elif sort == "shortest":
        sessions = sessions.order_by(
            "duration_minutes",
            "-date",
        )

    else:
        sessions = sessions.order_by(
            "-date",
            "-created_at",
        )

    # Pagination
    paginator = Paginator(
        sessions,
        5,
    )

    page_number = request.GET.get("page")

    page_obj = paginator.get_page(
        page_number
    )

    technologies = Technology.objects.order_by(
        "category",
        "name",
    )

    context = {
        "page_obj": page_obj,
        "technologies": technologies,

        "query": query,
        "selected_technology": technology_id,
        "date_from": date_from,
        "date_to": date_to,
        "min_duration": min_duration,
        "selected_sort": sort,
    }

    return render(
        request,
        "tracker/session_list.html",
        context,
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

    github_url = None

    if session.github_commit:
        github_url = (
            f"https://github.com/mohlaroy1/DailyDev/commit/"
            f"{session.github_commit}"
        )

    return render(
        request,
        "tracker/session_detail.html",
        {
            "session": session,
            "github_url": github_url,
        },
    )


@login_required
def session_edit(request, session_id):
    session = get_object_or_404(
        CodingSession,
        id=session_id,
        user=request.user,
    )

    if request.method == "POST":
        form = CodingSessionForm(
            request.POST,
            instance=session,
        )

        if form.is_valid():
            form.save()

            return redirect(
                "session_detail",
                session_id=session.id,
            )

    else:
        form = CodingSessionForm(
            instance=session
        )

    return render(
        request,
        "tracker/session_edit.html",
        {
            "form": form,
            "session": session,
        },
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

    total_duration = (
        user_sessions.aggregate(total=Sum("duration_minutes"))["total"]
        or 0
    )

    total_technologies = (
        user_sessions.values("technologies").distinct().count()
    )

    latest_session = user_sessions.order_by(
        "-date",
        "-created_at"
    ).first()

    today = timezone.localdate()

    week_start = today - timedelta(days=today.weekday())

    week_sessions = user_sessions.filter(
        date__gte=week_start,
        date__lte=today,
    )

    sessions_this_week = week_sessions.count()

    week_duration = (
        week_sessions.aggregate(total=Sum("duration_minutes"))["total"]
        or 0
    )

    most_used_technology = (
        user_sessions
        .values("technologies__name")
        .annotate(session_count=Count("id"))
        .order_by(
            "-session_count",
            "technologies__name",
        )
        .first()
    )

    session_dates = set(
        user_sessions.values_list("date", flat=True)
    )

    streak = 0
    current_day = today

    if current_day not in session_dates:
        current_day = today - timedelta(days=1)

    while current_day in session_dates:
        streak += 1
        current_day -= timedelta(days=1)

    daily_activity = []

    for i in range(6, -1, -1):

        day = today - timedelta(days=i)

        day_sessions = user_sessions.filter(date=day)

        day_duration = (
            day_sessions.aggregate(
                total=Sum("duration_minutes")
            )["total"]
            or 0
        )

        daily_activity.append({
            "date": day,
            "sessions": day_sessions.count(),
            "duration": day_duration,
        })

    context = {
        "total_sessions": total_sessions,
        "total_duration": total_duration,
        "total_technologies": total_technologies,
        "latest_session": latest_session,
        "sessions_this_week": sessions_this_week,
        "week_duration": week_duration,
        "most_used_technology": most_used_technology,
        "streak": streak,
        "daily_activity": daily_activity,
    }

    return render(
        request,
        "tracker/dashboard.html",
        context,
    )