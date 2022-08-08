from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (
    CardsAPIView,
    DecksAPIView,
    CardAnswersAPIView,
    PresetDecksAPIView,
    AddPresetDeckToUserDeckAPIView,
    MyLearningTableAPIView,
    ConsecutiveDaysAPIView,
)
from memo.views import DecksAPIView

router = DefaultRouter()
router.register("decks", DecksAPIView, basename="decks")
urlpatterns = router.urls

app_name = "memo"

urlpatterns = [
    path("cards/<int:pk>/", CardsAPIView.as_view(), name="card"),
    path("cards/", CardsAPIView.as_view(), name="cards"),
    path(
        "cards/<int:pk>/card-answer/", CardAnswersAPIView.as_view(), name="card_answers"
    ),
    path("card-answer/", CardAnswersAPIView.as_view(), name="answer_card"),
    path("preset-decks/", PresetDecksAPIView.as_view(), name="preset_decks"),
    path(
        "preset-decks/<int:pk>/add-to-decks/",
        AddPresetDeckToUserDeckAPIView.as_view(),
        name="preset_deck_to_deck",
    ),
    path(
        "my-learning-results/",
        MyLearningTableAPIView.as_view(),
        name="my_learning_result",
    ),
    path(
        "consecutive-days/",
        ConsecutiveDaysAPIView.as_view(),
        name="consecutive-days",
    ),
]
