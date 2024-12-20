from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from bank_account.bank.models import BankAccount, Transaction
from .serializers import (
    BankAccountSerializer,
    TransferSerializer,
    WithdrawDepositSerializer,
)


class BankAccountCreateAPIView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BankAccountSerializer
    queryset = BankAccount.objects.all()

    def get_serializer_context(self):
        return {"request": self.request}


class BankAccountDetailAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BankAccountSerializer

    def get_queryset(self):
        return BankAccount.objects.filter(user=self.request.user)


class DepositAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WithdrawDepositSerializer

    def post(self, request: Request, pk: int, *args, **kwargs) -> Response:
        account: BankAccount = get_object_or_404(BankAccount, pk=pk, user=request.user)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data["amount"]
            if amount > 0:
                account.balance += amount
                account.save()
                Transaction.objects.create(
                    bank_account=account, amount=amount, transaction_type="deposit"
                )
                return Response({"balance": account.balance}, status=HTTP_200_OK)
            return Response(
                {"error": "Invalid deposit amount"}, status=HTTP_400_BAD_REQUEST
            )
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class WithdrawAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WithdrawDepositSerializer

    def post(self, request: Request, pk: int, *args, **kwargs) -> Response:
        account: BankAccount = get_object_or_404(BankAccount, pk=pk, user=request.user)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data["amount"]
            if amount > 0 and account.balance >= amount:
                account.balance -= amount
                account.save()
                Transaction.objects.create(
                    bank_account=account, amount=amount, transaction_type="withdrawal"
                )
                return Response({"balance": account.balance}, status=HTTP_200_OK)
            return Response(
                {"error": "Insufficient funds or invalid amount"},
                status=HTTP_400_BAD_REQUEST,
            )
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class TransferAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TransferSerializer

    def post(self, request: Request, pk: int, *args, **kwargs) -> Response:
        debit_account = get_object_or_404(BankAccount, pk=pk, user=request.user)
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            receiver_account_number = serializer.validated_data["transfer_to"]
            amount = serializer.validated_data["amount"]

            credit_account = get_object_or_404(
                BankAccount, account_number=receiver_account_number
            )

            # ! prevent self account transfer.
            if debit_account.account_number == receiver_account_number:
                return Response(
                    {"error": "You cannot transfer money to the same account."},
                    status=HTTP_400_BAD_REQUEST,
                )
            if amount > 0 and debit_account.balance >= amount:
                with transaction.atomic():
                    debit_account.balance -= amount
                    debit_account.save()

                    credit_account.balance += amount
                    credit_account.save()

                    Transaction.objects.create(
                        bank_account=debit_account,
                        amount=amount,
                        transaction_type="transfer",
                    )

                return Response({"balance": debit_account.balance}, status=HTTP_200_OK)

            return Response(
                {"error": "Insufficient funds or invalid amount"},
                status=HTTP_400_BAD_REQUEST,
            )
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
