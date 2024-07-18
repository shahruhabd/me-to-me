from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from .models import Bank, Card, Balance, Transaction
from .serializers import BankSerializer, CardSerializer, BalanceSerializer, TransactionSerializer
from users.models import User
from django.db import transaction as db_transaction
from decimal import Decimal

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
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def transfer(request):
    hashed_id = request.data.get('hashed_id')
    amount = Decimal(request.data.get('amount'))  # Преобразуем в Decimal
    from_account = request.data.get('fromAccount')
    to_account = request.data.get('toAccount')

    try:
        user = User.objects.get(hashed_id=hashed_id)
        from_card = Card.objects.get(card_number=from_account, user=user)
        to_card = Card.objects.get(card_number=to_account, user=user)

        from_balance = Balance.objects.get(card=from_card)
        to_balance = Balance.objects.get(card=to_card)

        if from_balance.amount >= amount:
            with db_transaction.atomic():
                from_balance.amount -= amount
                to_balance.amount += amount

                from_balance.save()
                to_balance.save()

                Transaction.objects.create(
                    user=user,
                    amount=amount,
                    from_bank=from_card.bank,
                    to_bank=to_card.bank,
                    type='TRANSFER',
                    status='COMPLETED'
                )

            return Response({'message': 'Transfer completed successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Insufficient balance'}, status=status.HTTP_400_BAD_REQUEST)

    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except Card.DoesNotExist:
        return Response({'error': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)
    except Balance.DoesNotExist:
        return Response({'error': 'Balance not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)