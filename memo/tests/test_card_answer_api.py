from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
from decouple import config
from model_bakery import baker
from utils import convert_timestamp
from memo.models import CardAnswerHistory


class CardAnswerHistoryTest(APITestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_superuser(
            username="user", email="user@user.com", password="123"
        )

        self.user2 = self.User.objects.create_superuser(
            username="user2", email="user2@user.com", password="123"
        )

        token, created = Token.objects.get_or_create(user=self.user)
        self.assertTrue(created)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        self.url = config("HOST_VAR") + "/api/cards/"
        self.url_create = config("HOST_VAR") + "/api/card_answer/"

        self.deck = baker.make("Deck", owner=self.user)
        self.card = baker.make("Card", owner=self.user, deck=self.deck)
        self.data = {
            "correct": False,
            "card": self.card.id,
            "user_answer": "Test",
            "front": "Test",
            "back": "Testing",
        }
        self.card_answer = baker.make(
            "CardAnswerHistory", card=self.card, owner=self.user
        )

    def test_created_two_card_answers(self):
        self.assertEqual(1, CardAnswerHistory.objects.count())

    def test_get_card_answer_require_authorization(self):
        self.client.credentials()

        response = self.client.get(self.url + str(self.card.id) + "/card_answer/")
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_get_card_answer_success(self):
        response = self.client.get(self.url + str(self.card.id) + "/card_answer/")

        created_at = convert_timestamp(self.card_answer.created_at)

        expected_data = [
            {
                "id": self.card_answer.id,
                "correct": self.card_answer.correct,
                "card": self.card.id,
                "user_answer": self.card_answer.user_answer,
                "created_at": created_at,
            }
        ]

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(1, len(response.data))
        self.assertEqual(expected_data, response.data)

    def test_create_card_answer_success(self):
        response = self.client.post(self.url_create, self.data, format="json")

        card_history_id = response.data["id"]
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(2, CardAnswerHistory.objects.count())
        self.assertEqual(
            CardAnswerHistory.objects.get(id=card_history_id).correct,
            self.data["correct"],
        )
