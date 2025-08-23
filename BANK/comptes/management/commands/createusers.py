from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Create default admin and client users.'

    def add_arguments(self, parser):
        parser.add_argument('--admin-username', default='admin')
        parser.add_argument('--admin-password', default='admin123')
        parser.add_argument('--client-username', default='client')
        parser.add_argument('--client-password', default='client123')
        parser.add_argument('--extra-clients', type=int, default=0, help='Create N extra clients client1..clientN with password client123')

    def handle(self, *args, **options):
        User = get_user_model()
        admin_username = options['admin_username']
        admin_password = options['admin_password']
        client_username = options['client_username']
        client_password = options['client_password']
        created_any = False

        admin_user, created = User.objects.get_or_create(username=admin_username, defaults={'role': 'ADMIN'})
        if created:
            admin_user.set_password(admin_password)
            admin_user.is_staff = True
            admin_user.is_superuser = True
            admin_user.can_login = True if hasattr(admin_user, 'can_login') else admin_user.is_active
            admin_user.save()
            self.stdout.write(self.style.SUCCESS(f"Created admin user '{admin_username}'"))
            created_any = True
        else:
            self.stdout.write(f"Admin user '{admin_username}' already exists.")

        client_user, created = User.objects.get_or_create(username=client_username, defaults={'role': 'CLIENT'})
        if created:
            client_user.set_password(client_password)
            client_user.is_staff = False
            client_user.is_superuser = False
            client_user.can_login = True if hasattr(client_user, 'can_login') else client_user.is_active
            client_user.save()
            self.stdout.write(self.style.SUCCESS(f"Created client user '{client_username}'"))
            created_any = True
        else:
            self.stdout.write(f"Client user '{client_username}' already exists.")

        extra = options['extra_clients']
        for i in range(1, extra + 1):
            username = f"client{i}"
            user, created = User.objects.get_or_create(username=username, defaults={'role': 'CLIENT'})
            if created:
                user.set_password(client_password)
                if hasattr(user, 'can_login'):
                    user.can_login = True
                user.save()
                self.stdout.write(self.style.SUCCESS(f"Created client user '{username}'"))
                created_any = True

        if not created_any:
            self.stdout.write("No users created. All users already exist.")