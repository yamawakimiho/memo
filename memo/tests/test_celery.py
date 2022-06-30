from django.test import TestCase, override_settings
from memo.models import CardList
from model_bakery import baker
from django.contrib.auth import get_user_model
from django.core import mail
from project.tasks import send_email_task
from unittest.mock import patch


class TestCelery(TestCase):
    def setUp(self):
        self.User = get_user_model()
        self.user = self.User.objects.create_superuser(
            username="user", email="cab235@gmail.com", password="123"
        )

        self.deck = baker.make("CardList", owner=self.user)

    def test_celery_email_sent(self):
        self.assertEqual(1, CardList.objects.count())

        send_email_task(self.user)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "Your daily reminder - Memo")
        self.assertEqual(mail.outbox[0].to, ["cab235@gmail.com"])

    def test_celery_email_not_sent(self):
        CardList.objects.filter(id=self.deck.id).update(active=False)

        send_email_task(self.user)
        self.assertEqual(len(mail.outbox), 0)
