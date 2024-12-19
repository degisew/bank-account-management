from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from bank_account.bank.models import BankAccount, Transaction
from .serializers import BankAccountSerializer, WithdrawDepositSerializer


class BankAccountCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BankAccountSerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        data = request.data
        # data["user"] = request.user.id
        serializer = self.serializer_class(data=data, context={"request": request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class BankAccountDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BankAccountSerializer

    def get(self, request: Request, pk: int, *args, **kwargs) -> Response:
        account: BankAccount = get_object_or_404(BankAccount, pk=pk, user=request.user)
        serializer = self.serializer_class(account)
        return Response(serializer.data, status=HTTP_200_OK)


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
