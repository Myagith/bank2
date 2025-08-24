from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone


class Command(BaseCommand):
    help = "Crée des utilisateurs par défaut: admin/Admin123! et quelques clients."

    def handle(self, *args, **options):
        User = get_user_model()

        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={'email': 'admin@bank.local', 'role': 'ADMIN', 'can_login': True}
        )
        if created:
            admin.set_password('Admin123!')
            admin.save()
            self.stdout.write(self.style.SUCCESS('Admin créé: admin / Admin123!'))
        else:
            self.stdout.write('Admin déjà présent.')

        # Clients démo
        defaults = [
            ('alice', 'alice@demo.ci'),
            ('bob', 'bob@demo.ci'),
            ('charlie', 'charlie@demo.ci'),
        ]
        for username, email in defaults:
            user, created = User.objects.get_or_create(
                username=username,
                defaults={'email': email, 'role': 'CLIENT', 'can_login': True}
            )
            if created:
                user.set_password('Client123!')
                user.save()
                self.stdout.write(self.style.SUCCESS(f'Client créé: {username} / Client123!'))
            else:
                self.stdout.write(f'Client déjà présent: {username}')

        self.stdout.write(self.style.SUCCESS('Utilisateurs par défaut prêts.'))

