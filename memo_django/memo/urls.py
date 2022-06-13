from django.urls import path
# from rest_framework.routers import SimpleRouter
from .views import CardsAPIView, DecksAPIView, DeckAPIView

# router = SimpleRouter()
# router.register('card_lists', CardListViewSet)
# router.register('cards', CardViewSet, basename="card")
# router.register('cards_answers_history', CardAnswerHistoryViewSet)

app_name = 'memo'

urlpatterns = [
    path('decks/<int:pk>/', DeckAPIView.as_view(), name="deck"),
    path('decks/', DecksAPIView.as_view(), name="decks"),
    path('cards/', CardsAPIView.as_view(), name='cards'),
    path('cards/<int:pk>/', CardsAPIView.as_view(), name='card')
    
]