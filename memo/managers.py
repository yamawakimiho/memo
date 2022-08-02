import datetime
from django.db import models
from django.db.models import Count, Q, FloatField, Avg, Sum, Max
from django.db.models.functions import Cast


class CardManager(models.Manager):
    def get_filter_by_deck(self, deck):
        return (
            super(CardManager, self)
            .get_queryset()
            .filter(deck_id=deck, card_answers__isnull=False)
        )

    def get_total_answer(self, deck):
        return (
            self.get_filter_by_deck(deck)
            .annotate(total_answers=Count("card_answers"))
            .aggregate(Sum("total_answers"))
            .get("total_answers__sum")
        )

    def get_last_response(self, deck):
        last_response = (
            self.get_filter_by_deck(deck)
            .annotate(last_response=Max("card_answers__updated_at"))
            .aggregate(Max("last_response"))
            .get("last_response__max")
        )

        if last_response:
            last_response = datetime.datetime.astimezone(last_response).strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        return last_response

    def get_card_with_highest_mistaken(self, deck):
        return list(
            self.get_filter_by_deck(deck)
            .annotate(
                highest_mistaken_percentage=Cast(
                    Count("card_answers", filter=Q(card_answers__correct=False))
                    * 100
                    / Count("card_answers"),
                    FloatField(),
                )
            )
            .values_list("front", "highest_mistaken_percentage")
            .exclude(highest_mistaken_percentage=0)
            .order_by("-highest_mistaken_percentage")[:1]
        )

    def get_average_percentage_of_correct_answers(self, deck):
        return (
            self.filter(deck_id=deck, card_answers__isnull=False)
            .annotate(
                percent_of_correct_answers=Cast(
                    Count("card_answers", filter=Q(card_answers__correct=True))
                    * 100
                    / Count("card_answers"),
                    FloatField(),
                ),
            )
            .aggregate(Avg("percent_of_correct_answers"))
            .get("percent_of_correct_answers__avg")
        )

    def get_card_amount_in_deck(self, deck):
        return self.filter(deck=deck).count()


class DeckManager(models.Manager):
    def get_decks_by_owner(self, user):
        return self.filter(owner=user)
