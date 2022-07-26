from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
from decouple import config
from model_bakery import baker
from utils import convert_timestamp
from memo.models import Card


class MyLearningResultsTest(APITestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_superuser(
            username="user", email="user@user.com", password="123"
        )

        token, created = Token.objects.get_or_create(user=self.user)
        self.assertTrue(created)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        self.url = config("HOST_VAR") + "/api/my-learning-results/"

        self.deck = baker.make("Deck", owner=self.user)
        self.card = baker.make("Card", owner=self.user, deck=self.deck)
        self.card_answer = baker.make(
            "CardAnswerHistory", card=self.card, owner=self.user, correct=True
        )
        self.card_answer2 = baker.make(
            "CardAnswerHistory", card=self.card, owner=self.user, correct=False
        )
        self.card2 = baker.make("Card", owner=self.user, deck=self.deck)

    def test_get_my_learning_results(self):
        response = self.client.get(self.url)

        expected_data = [
            {
                "deck_name": self.deck.name,
                "amount_of_cards": Card.objects.get_card_amount_in_deck(self.deck),
                "last_response": convert_timestamp(self.card_answer2.created_at),
                "average_percentage_of_correct_answers": Card.objects.get_average_percentage_of_correct_answers(
                    self.deck
                ),
                "total_deck_response": Card.objects.get_total_answer(self.deck),
                "card_with_highest_mistaken": Card.objects.get_card_with_highest_mistaken(
                    self.deck
                ),
            }
        ]

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected_data, response.data)
