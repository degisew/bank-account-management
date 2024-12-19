# Create your models here.
from typing import Any
from django.db import models
from django.conf import settings
from model_utils.models import TimeStampedModel


class BankAccount(TimeStampedModel):
    """
    A model for representing bank accounts.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=20, unique=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self) -> str:
        return self.account_number

    def deposit(self, amount: float) -> Any | None:
        if amount > 0:
            self.balance += amount
            self.save()
            return self.balance
        return None

    def withdraw(self, amount: float) -> Any | None:
        if 0 < amount <= self.balance:
            self.balance -= amount
            self.save()
            return self.balance
        return None


class Transaction(TimeStampedModel):
    TRANSACTION_TYPES = (
        ("deposit", "Deposit"),
        ("withdrawal", "Withdrawal"),
        ("transfer", "Transfer"),
    )
    bank_account = models.ForeignKey(
        BankAccount, related_name="transactions", on_delete=models.CASCADE
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(choices=TRANSACTION_TYPES, max_length=20)

    def __str__(self) -> str:
        return (
            f"{self.transaction_type.capitalize()} - {self.bank_account.account_number}"
        )
