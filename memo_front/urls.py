from django.urls import path
from .views import card_list, assigment

app_name = "memo_front"

urlpatterns = [
    path("list/<slug:deck_id>/", card_list, name="card_list"),
    path("assigment/<slug:deck_id>/", assigment, name="assigment"),
]
