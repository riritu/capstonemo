from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Create admin user if it does not exist'

    def handle(self, *args, **options):
        username = 'trilc'
        password = 'trilcenterprises'

        if not User.objects.filter(username=username).exists():
            User.objects.create(username=username, password=make_password(password))
            self.stdout.write(self.style.SUCCESS('Admin user created successfully'))
        else:
            self.stdout.write(self.style.SUCCESS('Admin user already exists'))