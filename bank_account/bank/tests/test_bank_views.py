import pytest


@pytest.mark.django_db
def test_create_bank_account(api_client, user):
    api_client.force_authenticate(user=user)

    response = api_client.post("/accounts/", {"account_number": "1234567890"})
    assert response.status_code == 201
    assert response.data["account_number"] == "1234567890"


@pytest.mark.django_db
def test_get_bank_account_details(api_client, user, bank_account):
    api_client.force_authenticate(user=user)

    response = api_client.get(f"/accounts/{bank_account.id}/")
    assert response.status_code == 200
    assert response.data["account_number"] == bank_account.account_number
    # assert response.data["balance"] == f"BIRR {bank_account.balance}"


@pytest.mark.django_db
def test_deposit(api_client, user, bank_account):
    api_client.force_authenticate(user=user)

    response = api_client.post(
        f"/accounts/{bank_account.id}/deposit/", {"amount": 100.0}
    )
    assert response.status_code == 200
    assert response.data["balance"] == bank_account.balance + 100.0


@pytest.mark.django_db
def test_withdraw(api_client, user, bank_account):
    api_client.force_authenticate(user=user)

    response = api_client.post(
        f"/accounts/{bank_account.id}/withdraw/", {"amount": 200.0}
    )
    assert response.status_code == 200
    assert response.data["balance"] == bank_account.balance - 200.0

    response = api_client.post(
        f"/accounts/{bank_account.id}/withdraw/", {"amount": 1000.0}
    )
    assert response.status_code == 400
    assert response.data["error"] == "Insufficient funds or invalid amount"
