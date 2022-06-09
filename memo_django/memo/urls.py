
from rest_framework.routers import SimpleRouter
from .views import CardListViewSet, CardViewSet, CardAnswerHistoryViewSet

router = SimpleRouter()
router.register('card_lists', CardListViewSet)
router.register('cards', CardViewSet)
router.register('cards_answers_history', CardAnswerHistoryViewSet)
