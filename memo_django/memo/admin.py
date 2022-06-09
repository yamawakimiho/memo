from django.contrib import admin

from .models import Card, CardAnswerHistory, CardList

@admin.register(CardList)
class CardListAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at','updated_at','active','owner')

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('front', 'back', 'card_list', 'created_at','updated_at','active','owner')

@admin.register(CardAnswerHistory)
class CardAnswerHistoryAdmin(admin.ModelAdmin):
    list_display = ('user_answer', 'correct', 'created_at','card')

