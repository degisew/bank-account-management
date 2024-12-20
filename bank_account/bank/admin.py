from django.contrib import admin
from .models import Transaction, BankAccount


class TransactionInline(admin.TabularInline):
    model = Transaction


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    inlines = [
        TransactionInline,
    ]

    list_display = ("account_number", "balance")
