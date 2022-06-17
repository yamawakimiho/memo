from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from memo.urls import router

urlpatterns = [
    path("", include("accounts.urls"), name="accounts"),
    path("admin/", admin.site.urls),
    path("cards/", include("memo_front.urls"), name="cards"),
    path("api/", include("memo.urls"), name="memo"),
    path("api/", include(router.urls)),
]
