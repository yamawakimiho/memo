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
    my_field = serializers.SerializerMethodField()

    class Meta:
        model = PresetDeck
        fields = (
            "id",
            "name",
            "description",
            "preset_cards",
            "created_at",
            "updated_at",
            "my_field",
        )

    def get_my_field(self, obj):
        return now()
