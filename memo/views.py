from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView, Response
from rest_framework import authentication, permissions, status, viewsets, permissions
from .models import Card, CardAnswerHistory, Deck
from .serializers import DeckSerializer, CardSerializer, CardAnswerHistorySerializer


class DecksAPIView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DeckSerializer
    queryset = Deck.objects.all()

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user).order_by("-id")

    def destroy(self, request, *args, **kwargs):
        decks = self.get_object()
        if decks.owner_id == request.user.id:
            decks.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return super().update(request, *args, **kwargs)

    def perform_create(self, serializer_class):
        serializer_class.save(owner=self.request.user)


class CardAnswersAPIView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        if pk > 0:
            cards = CardAnswerHistory.objects.filter(card_id=pk).order_by("-id")
            serializer = CardAnswerHistorySerializer(cards, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CardAnswerHistorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CardsAPIView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = CardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)

    def put(self, request, pk):
        cards = get_object_or_404(Card, id=pk, owner=request.user)
        request.data["deck"] = cards.deck.id
        serializer = CardSerializer(cards, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            cards = Card.objects.get(owner=request.user, id=pk)
            cards.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
