from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    CardsAPIView,
    DecksAPIView,
    CardAnswersAPIView,
    PresetDecksAPIView,
    AddPresetDeckToUserDeckAPIView,
)
from memo.views import DecksAPIView

router = DefaultRouter()
router.register("decks", DecksAPIView, basename="decks")
urlpatterns = router.urls

app_name = "memo"

urlpatterns = [
    path("cards/<int:pk>/", CardsAPIView.as_view(), name="card"),
    path("cards/", CardsAPIView.as_view(), name="cards"),
    path("cards/", CardsAPIView.as_view(), name="cards"),
    path(
        "cards/<int:pk>/card_answer/", CardAnswersAPIView.as_view(), name="card_answers"
    ),
    path("card_answer/", CardAnswersAPIView.as_view(), name="answer_card"),
    path("preset_decks/", PresetDecksAPIView.as_view(), name="preset_decks"),
    path(
        "preset_decks/<int:pk>/add_to_decks/",
        AddPresetDeckToUserDeckAPIView.as_view(),
        name="preset_deck_to_deck",
    ),
]
