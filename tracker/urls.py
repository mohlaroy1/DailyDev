from django.urls import path
from . import views


urlpatterns = [
    path("", views.session_list, name="session_list"),
    path("sessions/new/", views.session_create, name="session_create"),
]