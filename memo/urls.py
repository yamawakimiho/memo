from django.urls import path
from .views import CardsAPIView, DecksAPIView, CardAnswersAPIView, CardAnswerAPIView
from memo.views import DecksAPIView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("decks", DecksAPIView, basename="decks")
urlpatterns = router.urls

app_name = "memo"

urlpatterns = [
    path("cards/<int:pk>/", CardsAPIView.as_view(), name="card"),
    path("cards/", CardsAPIView.as_view(), name="cards"),
    path(
        "cards/<int:pk>/card_answer/", CardAnswersAPIView.as_view(), name="answers_card"
    ),
    path("card_answer/", CardAnswerAPIView.as_view(), name="answer_card"),
]
