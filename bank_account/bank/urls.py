from django.urls import path
from bank_account.bank.api.views import (
    BankAccountCreateAPIView,
    BankAccountDetailAPIView,
    DepositAPIView,
    WithdrawAPIView,
    TransferAPIView,
)

urlpatterns = [
    path("", BankAccountCreateAPIView.as_view(), name="create_account"),
    path("<int:pk>/", BankAccountDetailAPIView.as_view(), name="account_detail"),
    path("<int:pk>/deposit/", DepositAPIView.as_view(), name="deposit"),
    path("<int:pk>/withdraw/", WithdrawAPIView.as_view(), name="withdraw"),
    path("<int:pk>/transfer/", TransferAPIView.as_view(), name="transfer"),
]
