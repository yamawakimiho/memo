from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework import status
from decouple import config
from model_bakery import baker
from utils import convertTimeStamp
from memo.models import Deck, PresetDeck


class PresetDeckTest(APITestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_superuser(
            username="user", email="user@user.com", password="123"
        )

        token, created = Token.objects.get_or_create(user=self.user)
        self.assertTrue(created)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        self.url = config("HOST_VAR") + "/api/preset_decks/"

        self.preset_deck = baker.make("PresetDeck", name="ABC")
        self.preset_card = baker.make("PresetCard", preset_deck=self.preset_deck)
        self.preset_deck2 = baker.make("PresetDeck", name="BAC")

        self.created_at = convertTimeStamp(self.preset_deck.created_at)

        self.updated_at = convertTimeStamp(self.preset_deck.updated_at)

    def test_created_preset_deck(self):
        self.assertEqual(2, PresetDeck.objects.count())

    def test_get_preset_decks_requires_authorization(self):
        self.client.credentials()

        response = self.client.get(self.url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_get_preset_decks_success(self):
        expected_data = {
            "count": 2,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.preset_deck.id,
                    "name": self.preset_deck.name,
                    "description": self.preset_deck.description,
                    "preset_cards": [
                        {
                            "id": self.preset_card.id,
                            "front": self.preset_card.front,
                            "back": self.preset_card.back,
                            "preset_deck": self.preset_deck.id,
                        }
                    ],
                    "created_at": self.created_at,
                    "updated_at": self.updated_at,
                },
                {
                    "id": self.preset_deck2.id,
                    "name": self.preset_deck2.name,
                    "description": self.preset_deck2.description,
                    "preset_cards": [],
                    "created_at": self.created_at,
                    "updated_at": self.updated_at,
                },
            ],
        }

        response = self.client.get(self.url, format="json")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected_data["count"], response.data["count"])
        self.assertEqual(expected_data, response.data)

    def test_copy_preset_deck_sucess(self):
        response = self.client.post(
            self.url + str(self.preset_deck.id) + "/add_to_decks/"
        )
        self.assertEqual(1, Deck.objects.count())
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

    def test_copy_preset_deck_error_not_found(self):
        response = self.client.post(self.url + str(99) + "/add_to_decks/")
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)
