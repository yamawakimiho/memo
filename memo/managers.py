from datetime import datetime, timedelta
from django.db import models
from django.db.models import Count, Q, FloatField, Avg, Sum, Max
from django.db.models.functions import Cast
from django.shortcuts import get_object_or_404


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
            .annotate(last_response=Max("card_answers__created_at"))
            .aggregate(Max("last_response"))
            .get("last_response__max")
        )

        if last_response:
            last_response = datetime.astimezone(last_response).strftime(
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


class CardAnswerHistoryManager(models.Manager):
    def get_consecutive_days(self, user):
        from .models import Card

        max_daily_date_times = (
            self.filter(owner=user)
            .extra(select={"day": "date( created_at )"})
            .values("day")
            .annotate(latest_datetime=Max("created_at"))
        )

        objects = (
            self.filter(
                created_at__in=[
                    entry["latest_datetime"] for entry in max_daily_date_times
                ]
            )
            .values("card", "created_at")
            .order_by("-created_at")
        )

        result = []

        if objects:
            answered_today = False
            today = datetime.today()
            count = 0
            one_day_less = 1

            for index in range(0, len(objects)):
                one_day_before = (today - timedelta(days=one_day_less)).strftime(
                    "%Y-%m-%d"
                )
                created_at = (objects[index].get("created_at")).strftime("%Y-%m-%d")

                if index == 0 and today.strftime("%Y-%m-%d") == created_at:
                    answered_today = True
                    count += 1
                    continue

                if created_at != one_day_before:
                    break

                count += 1
                one_day_less += 1

            card = get_object_or_404(Card, pk=objects[0].get("card"))

            result = {
                "consecutive_days": count,
                "card_front": card.front,
                "answered_today": answered_today,
                "last_answered_date": datetime.astimezone(
                    objects[0].get("created_at")
                ).strftime("%Y-%m-%d %H:%M:%S"),
            }

        return result
