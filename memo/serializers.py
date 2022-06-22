from rest_framework import serializers
from .models import CardAnswerHistory, CardList, Card


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
            "card_list",
            "created_at",
            "updated_at",
            "card_history",
        )


class CardListSerializer(serializers.ModelSerializer):
    cards = CardSerializer(many=True, read_only=True)

    class Meta:
        model = CardList
        fields = (
            "id",
            "name",
            "description",
            "cards",
            "created_at",
            "updated_at",
            "active",
        )
