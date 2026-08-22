from django.urls import path
from . import views


urlpatterns = [
    path("", views.session_list, name="session_list"),
]