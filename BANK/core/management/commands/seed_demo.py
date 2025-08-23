from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from decimal import Decimal
import random

from banks.models import Bank
from customers.models import Customer
from accounts.models import Account
from transactions.models import Transaction


class Command(BaseCommand):
    help = "Seed la base avec 15 banques, un admin, des clients, comptes et transactions."

    def handle(self, *args, **options):
        User = get_user_model()

        # Admin
        admin, created = User.objects.get_or_create(
            username='admin', defaults={'email': 'admin@bank.local', 'role': 'ADMIN', 'can_login': True}
        )
        if created:
            admin.set_password('Admin123!')
            admin.save()

        # Banks
        banks = []
        bank_names = [
            'Banque Atlantique','Société Générale CI','NSIA Banque','Bank of Africa','Ecobank','UBA','Versus Bank',
            'Bridge Bank','Coris Bank','BICICI','BACIM','FinBank','Orange Bank','Wizall Bank','Afriland Bank'
        ]
        for name in bank_names:
            bank, _ = Bank.objects.get_or_create(
                name=name,
                defaults={'country': 'Côte d\'Ivoire', 'city': 'Abidjan', 'email': f'contact@{name.lower().replace(" ","")}.ci', 'phone': '+22501020304'}
            )
            banks.append(bank)

        # Customers, Accounts and Transactions
        for i in range(1, 31):
            bank = random.choice(banks)
            customer, _ = Customer.objects.get_or_create(
                client_no=f'C{i:05d}', bank=bank,
                defaults={'name': f'Client {i}', 'email': f'client{i}@demo.ci', 'phone': '+22501020304'}
            )
            # Accounts
            for j in range(random.randint(1, 2)):
                acc, _ = Account.objects.get_or_create(
                    customer=customer,
                    number=f'CI{bank.id}{i:05d}{j:02d}',
                    defaults={'type': 'CHECKING', 'balance': Decimal('0.00')}
                )
                # Transactions
                for k in range(random.randint(3, 8)):
                    amount = Decimal(random.randint(10, 500))
                    ttype = random.choice(['DEPOSIT','WITHDRAW','TRANSFER'])
                    tx = Transaction.objects.create(account=acc, type=ttype, amount=amount, reference=f'DEMO-{i}-{j}-{k}')
                    # Update balance roughly (matching services.post_transaction logic simplified here)
                    if ttype == 'DEPOSIT' or ttype == 'TRANSFER':
                        acc.balance += amount
                    elif ttype == 'WITHDRAW' and acc.balance > amount:
                        acc.balance -= amount
                acc.save()

        self.stdout.write(self.style.SUCCESS('Seed terminé. Utilisateur admin/Admin123!'))

