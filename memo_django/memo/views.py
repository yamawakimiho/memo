from audioop import reverse
from urllib import request
from urllib.parse import urlencode
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views import View
from rest_framework import viewsets

from .models import Card, CardAnswerHistory, CardList
from .serializers import CardListSerializer, CardSerializer, CardAnswerHistorySerializer

class CardListViewSet(viewsets.ModelViewSet):
    queryset = CardList.objects.all()
    serializer_class = CardListSerializer
    
class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer

class CardAnswerHistoryViewSet(viewsets.ModelViewSet):
    queryset = CardAnswerHistory.objects.all()
    serializer_class = CardAnswerHistorySerializer
    