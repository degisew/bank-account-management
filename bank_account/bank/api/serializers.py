from rest_framework import serializers
from bank_account.bank.models import BankAccount, Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ["id", "bank_account", "amount", "transaction_type", "created"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation["amount"] = f"BIRR {instance.amount}"

        return representation


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

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation["balance"] = f"BIRR {instance.balance}"

        return representation


class TransferSerializer(serializers.Serializer):
    transfer_to = serializers.CharField(max_length=12)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)

    def validate_transfer_to(self, value):
        if not value.isdigit():
            raise serializers.ValidationError("Account number must be numeric.")
        if int(value) <= 0:
            raise serializers.ValidationError("Invalid account number.")
        return value
