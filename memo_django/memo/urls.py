from django.urls import path
from .views import CardsAPIView, DecksAPIView, DeckAPIView, CardAnswerAPIView

app_name = 'memo'

urlpatterns = [
    path('decks/<int:pk>/', DeckAPIView.as_view(), name="deck"),
    path('decks/', DecksAPIView.as_view(), name="decks"),
    path('cards/', CardsAPIView.as_view(), name='cards'),
    path('cards/<int:pk>/', CardsAPIView.as_view(), name='card'),
    path('card_answer/', CardAnswerAPIView.as_view(), name='card')
    
]