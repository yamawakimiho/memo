from rest_framework import serializers
from .models import CardAnswerHistory, Deck, Card, PresetCard, PresetDeck

from django.contrib.auth.models import User
from django.utils.timezone import now
from rest_framework import serializers


class CardAnswerHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CardAnswerHistory
        fields = (
            "id",
            "user_answer",
            "correct",
            "created_at",
            "card",
        )


class CardSerializer(serializers.ModelSerializer):
    card_history = CardAnswerHistorySerializer(
        many=True, read_only=True, source="card_answers"
    )

    class Meta:
        model = Card
        fields = (
            "id",
            "front",
            "back",
            "active",
            "deck",
            "created_at",
            "updated_at",
            "card_history",
        )


class DeckSerializer(serializers.ModelSerializer):
    cards = CardSerializer(many=True, read_only=True)

    class Meta:
        model = Deck
        fields = (
            "id",
            "name",
            "description",
            "cards",
            "created_at",
            "updated_at",
            "active",
        )


class PresetCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = PresetCard
        fields = ("id", "front", "back", "preset_deck")


class PresetDeckSerializer(serializers.ModelSerializer):
    preset_cards = PresetCardSerializer(many=True, read_only=True)

    class Meta:
        model = PresetDeck
        fields = (
            "id",
            "name",
            "description",
            "preset_cards",
            "created_at",
            "updated_at",
        )


class MyLearningTableSerializer(serializers.ModelSerializer):

    deck_name = serializers.CharField(source="name")
    amount_of_cards = serializers.SerializerMethodField()
    last_response = serializers.SerializerMethodField()
    average_percentage_of_correct_answers = serializers.SerializerMethodField()
    total_deck_response = serializers.SerializerMethodField()
    card_with_highest_mistaken = serializers.SerializerMethodField()

    def get_amount_of_cards(self, deck):
        return Card.objects.get_card_amount_in_deck(deck)

    def get_last_response(self, deck):
        return Card.objects.get_last_response(deck)

    def get_average_percentage_of_correct_answers(self, deck):
        return Card.objects.get_average_percentage_of_correct_answers(deck)

    def get_total_deck_response(self, deck):
        return Card.objects.get_total_answer(deck)

    def get_card_with_highest_mistaken(self, deck):
        return Card.objects.get_card_with_highest_mistaken(deck)

    class Meta:
        model = Deck
        fields = (
            "deck_name",
            "amount_of_cards",
            "last_response",
            "average_percentage_of_correct_answers",
            "total_deck_response",
            "card_with_highest_mistaken",
        )
