from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
from decouple import config
from model_bakery import baker
from memo.models import Card


class CardTest(APITestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_superuser(
            username="user", email="user@user.com", password="123"
        )

        token, created = Token.objects.get_or_create(user=self.user)
        self.assertTrue(created)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        self.url = config("HOST_VAR") + "/api/cards/"

        self.deck = baker.make("Deck", owner=self.user)
        self.data = {"front": "Testing", "back": "Testing2", "deck": self.deck.id}
        self.card = baker.make("Card", owner=self.user, deck=self.deck)
        self.card2 = baker.make("Card", owner=self.user, deck=self.deck)

    def test_created_two_cards(self):
        self.assertEqual(2, Card.objects.count())

    def test_create_card_requires_authorization(self):
        self.client.credentials()

        response = self.client.post(self.url, self.data, format="json")
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_create_card_success(self):
        response = self.client.post(self.url, self.data, format="json")

        card_id = response.data["id"]
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(3, Card.objects.count())
        self.assertEqual(Card.objects.get(id=card_id).front, self.data["front"])
        self.assertEqual(Card.objects.get(id=card_id).back, self.data["back"])

    def test_update_card_success(self):
        response = self.client.put(
            self.url + str(self.card.id) + "/", self.data, format="json"
        )

        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(Card.objects.get(id=self.card.id).front, self.data["front"])
        self.assertEqual(Card.objects.get(id=self.card.id).back, self.data["back"])

    def test_delete_card_created_by_same_authenticated_user_success(self):
        response = self.client.delete(self.url + str(self.card.id) + "/")
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
