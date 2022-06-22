import json
from rest_framework.authtoken.models import Token
from memo.models import CardList
from decouple import config
from rest_framework import status
from model_bakery import baker
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
import datetime

# https://www.django-rest-framework.org/api-guide/testing/
# https://model-bakery.readthedocs.io/en/latest/basic_usage.html


class CardListTest(APITestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_superuser(
            username="user", email="user@user.com", password="123"
        )

        token, created = Token.objects.get_or_create(user=self.user)
        self.assertTrue(created)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        self.url = config("HOST_VAR") + "/api/decks/"

        self.deck = baker.make("CardList", owner=self.user, description="testing")
        self.deck2 = baker.make("CardList", owner=self.user, description="testing")

        self.created_at = datetime.datetime.astimezone(self.deck.created_at).strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    def test_created_two_decks(self):
        self.assertEqual(2, CardList.objects.count())

    def test_get_decks_requires_authorization(self):
        self.client.credentials()

        response = self.client.get(self.url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_get_decks_success(self):
        response = self.client.get(self.url, format="json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(2, len(response.data))

        expected_data = [
            {
                "id": self.deck2.id,
                "name": self.deck2.name,
                "description": self.deck2.description,
                "cards": [],
                "created_at": self.created_at,
                "updated_at": self.created_at,
                "active": self.deck2.active,
            },
            {
                "id": self.deck.id,
                "name": self.deck.name,
                "description": self.deck.description,
                "cards": [],
                "created_at": self.created_at,
                "updated_at": self.created_at,
                "active": self.deck.active,
            },
        ]

        self.assertEqual(expected_data, response.data)

    def test_delete_deck_requires_authorization(self):
        self.client.credentials()

        response = self.client.delete(self.url + str(self.deck.id) + "/")
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_delete_deck_created_by_same_authenticated_user_success(self):
        response = self.client.delete(self.url + str(self.deck.id) + "/")
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_create_deck_success(self):

        data = {"name": "DeckTest", "description": "TestingDeck"}

        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(3, CardList.objects.count())

    def test_patch_deck_change_active_status_false(self):
        data = {"active": False}
        response = self.client.patch(
            self.url + str(self.deck.id) + "/", data, format="json"
        )

        expected_data = {
            "id": self.deck.id,
            "name": self.deck.name,
            "description": self.deck.description,
            "cards": [],
            "created_at": self.created_at,
            "updated_at": self.created_at,
            "active": False,
        }

        self.assertEqual(expected_data, response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_patch_deck_change_active_status_true(self):
        data = {"active": True}
        response = self.client.patch(
            self.url + str(self.deck.id) + "/", data, format="json"
        )

        expected_data = {
            "id": self.deck.id,
            "name": self.deck.name,
            "description": self.deck.description,
            "cards": [],
            "created_at": self.created_at,
            "updated_at": self.created_at,
            "active": True,
        }

        self.assertEqual(expected_data, response.data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
