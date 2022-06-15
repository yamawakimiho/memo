from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import status
from rest_framework.views import APIView, Response
from rest_framework import generics, viewsets, mixins, permissions
from .models import Card, CardAnswerHistory, CardList
from .serializers import CardListSerializer, CardSerializer, CardAnswerHistorySerializer

class DecksAPIView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None):
        try:
            context = {'request':request}
            if pk == None:
                cards = CardList.objects.all()
            else:
                cards = CardList.objects.filter(id=pk)
            serializer = CardListSerializer(cards, many=True, context=context)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except CardList.DoesNotExist:
            raise Http404

    def delete(self,request, pk):
        try: 
            card = CardList.objects.get(owner_id=request.user.id,id=pk)
            card.delete()
            return Response({"status":"1"}, status=status.HTTP_200_OK)
        except:
            return Response({"status":"0"}, status=status.HTTP_200_OK)

    def post(self,request):
        context = {'request':request}
        serializer = CardListSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save(owner_id=request.user.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)
class CardAnswersAPIView(generics.ListCreateAPIView):
    queryset = CardAnswerHistory.objects.all()
    serializer_class = CardAnswerHistorySerializer

    def get_queryset(self):
        if self.kwargs.get('pk'):
            return self.queryset.filter(card_id=self.kwargs.get('pk'))
        return self.queryset.all()

class CardAnswerAPIView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request):
        context = {'request':request}
        serializer = CardAnswerHistorySerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save(owner_id=request.user.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)
        
class CardsAPIView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request):
        context = {'request':request}
        serializer = CardSerializer(data=request.data, context=context)
        if serializer.is_valid():
            serializer.save(owner_id=request.user.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)

    def put(self, request, pk):
        context = {'request':request}
        cards = get_object_or_404(Card, id=pk,owner_id=request.user.id)
        request.data['card_list'] = cards.card_list.id
        serializer = CardSerializer(cards, data=request.data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response({"statis":1}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request, pk):
        try: 
            card = Card.objects.get(owner_id=request.user.id,id=pk)
            card.delete()
            return Response({"status":"1"}, status=status.HTTP_200_OK)
        except:
            return Response({"status":"0"}, status=status.HTTP_200_OK)