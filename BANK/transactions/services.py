from decimal import Decimal
from django.db import transaction as db_transaction
from .models import Transaction
from accounts.models import Account


@db_transaction.atomic
def post_transaction(tx: Transaction) -> None:
    account: Account = tx.account
    if tx.type == Transaction.Type.DEPOSIT:
        account.balance = (account.balance or Decimal('0')) + tx.amount
    elif tx.type == Transaction.Type.WITHDRAW:
        if (account.balance or Decimal('0')) < tx.amount:
            raise ValueError('Insufficient funds')
        account.balance -= tx.amount
    elif tx.type == Transaction.Type.TRANSFER:
        # For simplicity, a transfer is treated as deposit into same account in this demo.
        account.balance += tx.amount
    account.save(update_fields=['balance'])