from celery import shared_task
from decouple import config
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from memo.models import Deck


def send_email(user):
    deck_list = []

    decks = Deck.objects.filter(owner_id=user.id).all()

    for deck in decks:
        if deck.active == True:
            deck_list.append(deck.name)

    if len(deck_list) > 0:
        html_message = render_to_string(
            "email/reminder.txt",
            {"deck_list": deck_list, "username": user.username},
        )
        email = EmailMessage(
            "Your daily reminder - Memo",
            html_message,
            config("EMAIL_USER"),
            [user.email],
        )

        email.content_subtype = "html"
        email.send()


@shared_task
def send_email_task(users=False):

    if users:
        send_email(users)
        return "1 email sent"

    users = User.objects.all()
    for user in users:
        send_email(user)

    return "Email sent"
