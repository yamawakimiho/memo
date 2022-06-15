from django.urls import path
from .views import CardsAPIView, DecksAPIView, CardAnswerAPIView, CardAnswersAPIView

app_name = 'memo'

urlpatterns = [
    path('decks/<int:pk>/', DecksAPIView.as_view(), name="deck"),
    path('decks/', DecksAPIView.as_view(), name="decks"),
    path('cards/<int:pk>/', CardsAPIView.as_view(), name='card'),
    path('cards/', CardsAPIView.as_view(), name='card'),
    path('card_answer/', CardAnswerAPIView.as_view(), name='answers'),
    path('cards/<int:pk>/card_answer/', CardAnswersAPIView.as_view(), name='answers_card')
]