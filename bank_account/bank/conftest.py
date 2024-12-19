import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from django.contrib.auth import get_user_model
from bank_account.bank.models import BankAccount

User = get_user_model()


@pytest.fixture
def api_client() -> APIClient:
    """Fixture to provide an API client."""
    return APIClient()


@pytest.fixture
def user():
    """Fixture to create a user."""
    return baker.make(User)


@pytest.fixture
def bank_account(user) -> BankAccount:
    """Fixture to create a bank account for the user."""
    return baker.make(BankAccount, user=user, balance=500.00)
