from rest_framework import serializers
from .models import CardAnswerHistory, CardList, Card

class CardAnswerHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CardAnswerHistory
        fields = (
            'id',
            'user_answer',
            'correct',
            'updated_at',
            'owner',
            'card',
        )
        
class CardSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="owner.username",read_only=True)
    card_history = CardAnswerHistorySerializer(many=True, read_only=True, source='card_answers')
    
    class Meta:
        model = Card
        fields = (
            'id',
            'front',
            'back',
            'username',
            'card_list',
            'created_at',
            'updated_at',
            'card_history',
        )

class CardListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="owner.username",read_only=True)
    cards = CardSerializer(many=True, read_only=True)

    class Meta:
        model = CardList
        fields = (
            'id',
            'name',
            'description',
            'cards',
            'username',
            'created_at',
        )

