from django.urls import path
from .views import *

urlpatterns = [
    path('banks/', BankListView.as_view(), name='bank-list'),
    path('cards/<str:hashed_id>', UserCardsView.as_view(), name='user-cards'),
    path('balances/<str:hashed_id>', UserBalancesView.as_view(), name='user-balances'),
    path('transactions/<str:hashed_id>', UserTransactionsView.as_view(), name='user-transactions'),
]
