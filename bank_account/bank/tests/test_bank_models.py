import pytest
from model_bakery import baker

from bank_account.bank.models import BankAccount


@pytest.mark.django_db
def test_bank_account_balance_update():
    account = baker.make(BankAccount, balance=100.0)
    account.deposit(50.0)
    assert account.balance == 150.0
    account.withdraw(30.0)
    assert account.balance == 120.0
