from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.core.validators import MinLengthValidator

class Base(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=('Updated At'))
    active = models.BooleanField(default=True, verbose_name=('Active'))
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,verbose_name=('Owner'))
    class Meta:
        abstract = True

class CardList(Base):
    name = models.CharField(
        max_length=100,
        validators=[MinLengthValidator(2, "Card name must be grater than 2 characters")]
    )
    description = models.TextField(verbose_name=('Description'), blank=True, default='')

    def __str__(self):
        return self.name

class Card(Base):
    front = models.CharField(max_length=255, verbose_name=('Front'))
    back = models.CharField(max_length=255, verbose_name=('Back'))
    card_list = models.ForeignKey(CardList, related_name='cards', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.front}, {self.back}'

class CardAnswerHistory(Base):
    user_answer = models.CharField(max_length=255, verbose_name=('Answer'))
    correct = models.BooleanField(default=True, verbose_name=('Correct')) # is it correct or not?
    card = models.ForeignKey(Card, related_name='card_answers', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.card}: {self.user_answer}, {self.correct}'