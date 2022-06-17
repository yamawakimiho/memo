from django.urls import path
from . import views

app_name = "memo_front"

urlpatterns = [
    path("list/<slug:deck_id>/", views.card_list, name="card_list"),
    path("assigment/<slug:deck_id>/", views.assigment, name="assigment"),
]
