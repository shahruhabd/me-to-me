from rest_framework import serializers
from .models import Bank, Card, Balance, Transaction

class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = ['id', 'name']

class CardSerializer(serializers.ModelSerializer):
    bank = BankSerializer()

    class Meta:
        model = Card
        fields = '__all__'

class BalanceSerializer(serializers.ModelSerializer):
    card = CardSerializer()

    class Meta:
        model = Balance
        fields = '__all__'

class TransactionSerializer(serializers.ModelSerializer):
    from_bank = BankSerializer()
    to_bank = BankSerializer()

    class Meta:
        model = Transaction
        fields = ['id', 'status', 'amount', 'chargeAmount', 'type', 'createDateTime', 'from_bank', 'to_bank']
