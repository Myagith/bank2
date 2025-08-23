from decimal import Decimal
from django.db import transaction as db_transaction
from django.core.mail import send_mail
from django.conf import settings
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
    # Notify account owner (demo: send to account.customer.email)
    try:
        subject = f"{tx.type.title()} de {tx.amount}"
        message = f"Votre compte {account.number} a une opération: {tx.type} de {tx.amount}. Réf: {tx.reference}."
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [account.customer.email], fail_silently=True)
    except Exception:
        pass