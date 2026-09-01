from django.contrib import admin
from django.urls import path, include
from tracker import views


urlpatterns = [
    path("admin/", admin.site.urls),

    path("", views.session_list, name="session_list"),

    path("dashboard/", views.dashboard, name="dashboard"),

    path("sessions/new/", views.session_create, name="session_create"),

    path(
        "sessions/<int:session_id>/",
        views.session_detail,
        name="session_detail"
    ),

    path(
        "sessions/<int:session_id>/edit/",
        views.session_edit,
        name="session_edit"
    ),

    path(
        "sessions/<int:session_id>/delete/",
        views.session_delete,
        name="session_delete"
    ),

    # Authentication
    path("accounts/", include("django.contrib.auth.urls")),
]