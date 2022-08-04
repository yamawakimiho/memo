from datetime import datetime, timedelta
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
from decouple import config
from model_bakery import baker
from utils import convert_timestamp


class ConsecutiveDaysTest(APITestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_superuser(
            username="user", email="user@user.com", password="123"
        )

        token, _ = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        self.url = config("HOST_VAR") + "/api/consecutive-days/"

        self.deck = baker.make("Deck", owner=self.user)
        self.card = baker.make("Card", owner=self.user, deck=self.deck)

        self.card_answer = baker.make(
            "CardAnswerHistory", card=self.card, owner=self.user
        )

        self.card_answer2 = baker.make(
            "CardAnswerHistory",
            card=self.card,
            owner=self.user,
        )

        self.card_answer3 = baker.make(
            "CardAnswerHistory",
            card=self.card,
            owner=self.user,
        )

        self.today = datetime.today()

    def test_get_consecutive_days_results_sucess_answered_today(self):
        response = self.client.get(self.url)

        expected_data = {
            "consecutive_days": 1,
            "card_front": self.card.front,
            "answered_today": True,
            "last_answered_date": convert_timestamp(self.card_answer3.created_at),
        }

        self.assertEqual(expected_data, response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_consecutive_days_results_sucess_not_answered_today_no_streak(
        self,
    ):
        self.card_answer.created_at = self.today - timedelta(days=2)
        self.card_answer2.created_at = self.today - timedelta(days=2)
        self.card_answer3.created_at = self.today - timedelta(days=2)
        self.card_answer.save()
        self.card_answer2.save()
        self.card_answer3.save()

        response = self.client.get(self.url)

        expected_data = {
            "consecutive_days": 0,
            "card_front": self.card.front,
            "answered_today": False,
            "last_answered_date": convert_timestamp(self.card_answer3.created_at),
        }

        self.assertEqual(expected_data, response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_consecutive_days_results_display_consecutive_days_not_answered_today(
        self,
    ):
        self.card_answer.created_at = self.today - timedelta(days=3)
        self.card_answer2.created_at = self.today - timedelta(days=2)
        self.card_answer3.created_at = self.today - timedelta(days=1)
        self.card_answer.save()
        self.card_answer2.save()
        self.card_answer3.save()

        response = self.client.get(self.url)

        expected_data = {
            "consecutive_days": 3,
            "card_front": self.card.front,
            "answered_today": False,
            "last_answered_date": convert_timestamp(self.card_answer3.created_at),
        }

        self.assertEqual(expected_data, response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_consecutive_days_results_display_consecutive_days_answered_today(self):

        self.card_answer.created_at = self.today - timedelta(days=3)
        self.card_answer2.created_at = self.today - timedelta(days=2)
        self.card_answer3.created_at = self.today - timedelta(days=1)
        self.card_answer.save()
        self.card_answer2.save()
        self.card_answer3.save()

        card_answer4 = baker.make("CardAnswerHistory", card=self.card, owner=self.user)

        response = self.client.get(self.url)

        expected_data = {
            "consecutive_days": 4,
            "card_front": self.card.front,
            "answered_today": True,
            "last_answered_date": convert_timestamp(card_answer4.created_at),
        }

        self.assertEqual(expected_data, response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_get_consecutive_days_results_display_last_answered_card(self):

        self.card_answer.created_at = self.today - timedelta(days=3)
        self.card_answer2.created_at = self.today - timedelta(days=2)
        self.card_answer3.created_at = self.today - timedelta(days=1)
        self.card_answer.save()
        self.card_answer2.save()
        self.card_answer3.save()

        card2 = baker.make("Card", owner=self.user, deck=self.deck)
        card_answer4 = baker.make("CardAnswerHistory", card=card2, owner=self.user)

        response = self.client.get(self.url)

        expected_data = {
            "consecutive_days": 4,
            "card_front": card2.front,
            "answered_today": True,
            "last_answered_date": convert_timestamp(card_answer4.created_at),
        }

        self.assertEqual(expected_data, response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
