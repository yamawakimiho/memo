from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView, Response
from rest_framework import authentication, permissions, status, viewsets, generics
from .models import Card, CardAnswerHistory, Deck, PresetCard, PresetDeck
from .serializers import (
    DeckSerializer,
    CardSerializer,
    CardAnswerHistorySerializer,
    PresetDeckSerializer,
)
from rest_framework.pagination import PageNumberPagination


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
        card = get_object_or_404(Card, id=pk, owner=request.user)
        request.data["deck"] = card.deck.id
        serializer = CardSerializer(card, data=request.data)
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


class CustomPageNumberPagination(PageNumberPagination):
    page_size = 9
    page_size_query_param = "rows"
    max_page_size = 100


class PresetDecksAPIView(generics.ListAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    queryset = PresetDeck.objects.all().order_by("name")
    serializer_class = PresetDeckSerializer
    pagination_class = CustomPageNumberPagination


class AddPresetDeckToUserDeckAPIView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        preset_deck = get_object_or_404(PresetDeck, id=pk)
        try:
            deck = Deck.objects.create(
                name=preset_deck.name,
                description=preset_deck.description,
                owner=request.user,
            )

            preset_cards = PresetCard.objects.filter(preset_deck_id=pk)

            for preset_card in preset_cards:
                Card.objects.create(
                    front=preset_card.front,
                    back=preset_card.back,
                    deck_id=deck.id,
                    owner=request.user,
                )
            return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class MyLearningTableAPIView(APIView):
    def get(self, request):
        my_learning = Deck.objects.get_my_learning_queryset(request.user)
        return Response(my_learning, status=status.HTTP_200_OK)
