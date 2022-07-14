from django.contrib import admin
from django.urls import path, include
from memo_front.views import redirect_if_not_logged, register_request, presets
from memo.urls import router

urlpatterns = [
    path("", redirect_if_not_logged, name="index"),
    path("presets/", presets, name="presets"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("acounts/register/", register_request, name="register"),
    path("admin/", admin.site.urls),
    path("cards/", include("memo_front.urls"), name="cards"),
    path("api/", include("memo.urls"), name="memo"),
    path("api/", include(router.urls)),
]
