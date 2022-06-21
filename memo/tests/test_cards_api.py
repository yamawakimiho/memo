from rest_framework.authtoken.models import Token
from memo.models import Card
from decouple import config
from rest_framework import status
from model_bakery import baker
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase


class CardTest(APITestCase):
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

        self.deck = baker.make("CardList", owner=self.user)
        self.data = {"front": "Testing", "back": "Testing2", "card_list": self.deck.id}
        self.card = baker.make("Card", owner=self.user, card_list=self.deck)
        self.card2 = baker.make("Card", owner=self.user2, card_list=self.deck)

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

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(Card.objects.get(id=self.card.id).front, self.data["front"])
        self.assertEqual(Card.objects.get(id=self.card.id).back, self.data["back"])

    def test_update_card_created_by_another_user_fail(self):
        response = self.client.put(
            self.url + str(self.card2.id) + "/", self.data, format="json"
        )

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_delete_card_created_by_same_authenticated_user_success(self):
        response = self.client.delete(self.url + str(self.card.id) + "/")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual({"status": "1"}, response.data)

    def test_delete_card_created_by_another_user_fail(self):
        response = self.client.delete(self.url + str(self.card2.id) + "/")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual({"status": "0"}, response.data)
