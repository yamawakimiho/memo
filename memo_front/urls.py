from django.urls import path
from .views import deck, assigment

app_name = "memo_front"

urlpatterns = [
    path("deck/<slug:deck_id>/", deck, name="deck"),
    path("assigment/<slug:deck_id>/", assigment, name="assigment"),
]
