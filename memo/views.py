from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import status
from rest_framework.views import APIView, Response
from rest_framework import generics, permissions
from .models import Card, CardAnswerHistory, CardList
from .serializers import CardListSerializer, CardSerializer, CardAnswerHistorySerializer


class DecksAPIView(viewsets.ModelViewSet):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CardListSerializer
    queryset = CardList.objects.all().order_by("-id")

    def destroy(self, request, *args, **kwargs):
        decks = self.get_object()
        if decks.owner_id == request.user.id:
            decks.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
            )

    def perform_create(self, serializer_class):
        serializer_class.save(owner=self.request.user)


class CardAnswersAPIView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        if pk > 0:
            cards = CardAnswerHistory.objects.filter(
                card_id=self.kwargs.get("pk")
            ).order_by("-id")
            serializer = CardAnswerHistorySerializer(
                cards, many=True, context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = CardAnswerHistorySerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save(owner_id=request.user.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)


class CardsAPIView(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = CardSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            serializer.save(owner_id=request.user.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)

    def put(self, request, pk):
        cards = get_object_or_404(Card, id=pk, owner_id=request.user.id)
        request.data["card_list"] = cards.card_list.id
        serializer = CardSerializer(cards, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "1"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            cards = Card.objects.get(owner_id=request.user.id, id=pk)
            cards.delete()
            return Response({"status": "1"}, status=status.HTTP_200_OK)
        except:
            return Response({"status": "0"}, status=status.HTTP_200_OK)
