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
    hashed_id = request.data.get('hashedId')
    amount = request.data.get('amount')
    from_account = request.data.get('fromAccount')
    to_account = request.data.get('toAccount')
    charge_amount = request.data.get('chargeAmount', 0)

    print(f"hashed_id: {hashed_id}, amount: {amount}, from_account: {from_account}, to_account: {to_account}, charge_amount: {charge_amount}")

    try:
        user = User.objects.get(hashed_id=hashed_id)
        print(f"User found: {user}")
        from_card = Card.objects.get(card_number=from_account, user=user)
        print(f"From card found: {from_card}")
        to_card = Card.objects.get(card_number=to_account, user=user)
        print(f"To card found: {to_card}")

        from_balance = Balance.objects.get(card=from_card)
        to_balance = Balance.objects.get(card=to_card)

        if from_balance.amount >= Decimal(amount):
            with db_transaction.atomic():
                from_balance.amount -= Decimal(amount)
                to_balance.amount += Decimal(amount)

                from_balance.save()
                to_balance.save()

                Transaction.objects.create(
                    user=user,
                    amount=Decimal(amount),
                    chargeAmount=Decimal(charge_amount),
                    type='TRANSFER',
                    status='COMPLETED',
                    from_bank=from_card.bank,
                    to_bank=to_card.bank,
                )

            return Response({'message': 'Transfer completed successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Insufficient balance'}, status=status.HTTP_400_BAD_REQUEST)

    except User.DoesNotExist:
        print("User not found")
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    except Card.DoesNotExist:
        print("Card not found")
        return Response({'error': 'Account not found'}, status=status.HTTP_404_NOT_FOUND)
    except Balance.DoesNotExist:
        print("Balance not found")
        return Response({'error': 'Balance not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(f"Exception: {e}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
