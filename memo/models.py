from django.db import models
from django.conf import settings
from django.core.validators import MinLengthValidator


class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=("Updated At"))
    active = models.BooleanField(default=True, verbose_name=("Active"))
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name=("Owner")
    )

    class Meta:
        abstract = True


class Deck(Base):
    name = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(2, "Card name must be grater than 2 characters")
        ],
    )
    description = models.TextField(verbose_name=("Description"), blank=True, default="")

    class Meta:
        verbose_name_plural = "Decks"
        verbose_name = "Deck"
        
    def __str__(self):
        return self.name


class Card(Base):
    front = models.CharField(max_length=255, verbose_name=("Front"))
    back = models.CharField(max_length=255, verbose_name=("Back"))
    deck = models.ForeignKey(
        Deck, related_name="cards", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name_plural = "Cards"
        verbose_name = "Card"

    def __str__(self):
        return f"{self.front}, {self.back}"


class CardAnswerHistory(Base):
    user_answer = models.CharField(max_length=255, verbose_name=("Answer"))
    correct = models.BooleanField(
        default=True, verbose_name=("Correct")
    )  # is it correct or not?
    card = models.ForeignKey(
        Card, related_name="card_answers", on_delete=models.CASCADE
    )
    ordering = ["-id"]

    def __str__(self):
        return f"{self.card}: {self.user_answer}, {self.correct}"

class PresetDeck(Base):
    name = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(2, "Card name must be grater than 2 characters")
        ],
    )
    description = models.TextField(verbose_name=("Description"), blank=True, default="")
    active = None
    owner = None

    class Meta:
        verbose_name_plural = "Preset Decks"

    def __str__(self):
        return self.name

class PresetCard(Base):
    front = models.CharField(max_length=255, verbose_name=("Front"))
    back = models.CharField(max_length=255, verbose_name=("Back"))
    deck = models.ForeignKey(
        PresetDeck, related_name="cards", on_delete=models.CASCADE
    )
    active = None
    owner = None

    class Meta:
        verbose_name_plural = "Preset Cards"
        verbose_name = "Preset Cards"

    def __str__(self):
        return f"{self.front}, {self.back}"
