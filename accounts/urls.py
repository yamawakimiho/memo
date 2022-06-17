from django.urls import path, include
from django.views.generic import TemplateView
from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.redirect_if_not_logged, name="index"),
    path("accounts/", include("django.contrib.auth.urls")),  # new
]
