from django.contrib import admin

from .models import Card, CardAnswerHistory, Deck, PresetCard, PresetDeck


@admin.register(Deck)
class DeckAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "created_at",
        "updated_at",
        "active",
        "owner",
    )


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = (
        "front",
        "back",
        "deck",
        "created_at",
        "updated_at",
        "active",
        "owner",
    )


@admin.register(CardAnswerHistory)
class CardAnswerHistoryAdmin(admin.ModelAdmin):
    list_display = ("user_answer", "correct", "created_at", "card", "owner")

@admin.register(PresetCard)
class PresetCardAdmin(admin.ModelAdmin):
    list_display = (
        "front",
        "back",
        "deck",
        "created_at",
        "updated_at",
    )

@admin.register(PresetDeck)
class PresetDeckAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "description",
        "created_at",
        "updated_at",
    )
