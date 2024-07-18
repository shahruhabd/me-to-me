from django.contrib import admin
from .models import Bank, Card, Balance, Transaction

@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('user', 'bank', 'card_number', 'expiry_date', 'card_type')
    search_fields = ('user', 'bank__name', 'card_number')
    list_filter = ('card_type',)

@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
    list_display = ( 'amount', 'currency', 'card')
    search_fields = ('user__phone_number', 'user__iin', 'card__card_number')
    list_filter = ('currency',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'status', 'type', 'createDateTime', 'from_bank', 'to_bank')
    search_fields = ('user__phone_number', 'from_bank__name', 'to_bank__name')
    list_filter = ('status', 'type', 'createDateTime')
