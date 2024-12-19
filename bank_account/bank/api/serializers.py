from rest_framework import serializers
from bank_account.bank.models import BankAccount, Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["id", "bank_account", "amount", "transaction_type", "created"]


class WithdrawDepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["amount"]


class BankAccountSerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True, read_only=True)

    class Meta:
        model = BankAccount
        fields = ["id", "account_number", "balance", "transactions", "created"]

    def create(self, validated_data) -> BankAccount:
        user = self.context["request"].user
        return BankAccount.objects.create(user=user, **validated_data)
