from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import action, api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from django.contrib.auth.models import User
from django.db.models import Prefetch
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.views import APIView, Response

from .models import Card, CardAnswerHistory, CardList
from .serializers import CardListSerializer, CardSerializer, CardAnswerHistorySerializer

class DeckAPIView(APIView):
    def get(self, request, pk):
        context = {'request':request}
        cards = CardList.objects.filter(id=pk)
        serializer = CardListSerializer(cards, many=True, context=context)
        return Response(serializer.data, status=status.HTTP_200_OK)

class DecksAPIView(APIView):
    def post(this,request):
        context = {'request':request}
        print(request.data)
        serializer = CardListSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save(owner_id=request.user.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)

    def get(this,request):
        context = {'request':request}
        cards = CardList.objects.all()
        serializer = CardListSerializer(cards, many=True, context=context)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CardsAPIView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(this,request):
        context = {'request':request}
        serializer = CardSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save(owner_id=request.user.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)

    def get(this,request):
        context = {'request':request}
        cards = Card.objects.filter(owner_id=request.user.id)
        serializer = CardSerializer(cards, many=True, context=context)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(this,request, pk):
        try: 
            card = Card.objects.get(owner_id=request.user.id,id=pk)
            card.delete()
            return Response({"status":"1"}, status=status.HTTP_200_OK)
        except:
            return Response({"status":"0"}, status=status.HTTP_200_OK)