from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from memo_front.views import redirect_if_not_logged
from memo.urls import router

urlpatterns = [
    path("", redirect_if_not_logged, name="index"),
    path("accounts/", include("django.contrib.auth.urls")), 
    path("admin/", admin.site.urls),
    path("cards/", include("memo_front.urls"), name="cards"),
    path("api/", include("memo.urls"), name="memo"),
    path("api/", include(router.urls)),
]

# from django.conf import settings
# from django.conf.urls import include, static
# 
# import debug_toolbar
# urlpatterns += path('__debug__/', include(debug_toolbar.urls)),


