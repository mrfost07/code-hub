from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import IntegrityError

class Command(BaseCommand):
    help = 'Creates a superuser if it does not exist'

    def handle(self, *args, **options):
        try:
            if not User.objects.filter(username='admin').exists():
                User.objects.create_superuser(
                    username='admin',
                    email='admin@example.com',
                    password='admin12345'
                )
                self.stdout.write(self.style.SUCCESS('Superuser created successfully'))
            else:
                self.stdout.write(self.style.WARNING('Superuser already exists'))
        except IntegrityError:
            self.stdout.write(self.style.ERROR('Error creating superuser')) 