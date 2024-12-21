import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from django.contrib.auth import get_user_model
from bank_account.bank.models import BankAccount

User = get_user_model()


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture
def user():
    return baker.make(User)


@pytest.fixture
def bank_account(user) -> BankAccount:
    return baker.make(BankAccount, user=user, balance=500.00)
