from rest_framework import generics, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Bank, Card, Balance, Transaction
from .serializers import BankSerializer, CardSerializer, BalanceSerializer, TransactionSerializer
from users.models import User

class BankListView(generics.ListCreateAPIView):
    queryset = Bank.objects.all()
    serializer_class = BankSerializer
    permission_classes = [IsAuthenticated]

class UserCardsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CardSerializer

    def get_queryset(self):
        hashed_id = self.kwargs['hashed_id']
        user = User.objects.get(hashed_id=hashed_id)
        return Card.objects.filter(user=user)

class UserBalancesView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BalanceSerializer

    def get_queryset(self):
        hashed_id = self.kwargs['hashed_id']
        user = User.objects.get(hashed_id=hashed_id)
        cards = Card.objects.filter(user=user)
        return Balance.objects.filter(card__in=cards)

class UserTransactionsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionSerializer

    def get_queryset(self):
        hashed_id = self.kwargs['hashed_id']
        user = User.objects.get(hashed_id=hashed_id)
        return Transaction.objects.filter(user=user)