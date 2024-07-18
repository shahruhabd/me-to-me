from django.db import models
from users.models import User

class Bank(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16, unique=True)
    expiry_date = models.CharField(max_length=5)  # MM/YY формат
    cvv_code = models.CharField(max_length=3)
    card_type = models.CharField(max_length=10, choices=[('VISA', 'Visa'), ('MASTERCARD', 'MasterCard')])

    def __str__(self):
        return f'{self.bank.name} - {self.card_number}'

class Balance(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.card.user.iin} - {self.amount} {self.currency}'

class Transaction(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
    ]
    
    TYPE_CHOICES = [
        ('INCOME', 'Пополнение'),
        ('WITHDRAWAL', 'Снятие'),
        ('TRANSFER', 'Перевод'),
        ('PURCHASE', 'Покупка'),
        ('E_COMMERCE', 'Интернет покупка'),
        ('PAYMENT', 'Платеж'),
        ('BONUS', 'Бонус/кэшбек'),
        ('OTHER', 'Прочие операции'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    chargeAmount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    createDateTime = models.DateTimeField(auto_now_add=True)
    from_bank = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name='from_transactions')
    to_bank = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name='to_transactions')

    def __str__(self):
        return f'{self.user.phone_number} - {self.type} - {self.amount}'