from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import IntegrityError
import user.models as um


class Command(BaseCommand):
    """
    Create a superuser if none exist
    Example:
        manage.py createsuperuser_if_none_exists
    """

    def handle(self, *args, **options):
        user = get_user_model()
        password = settings.DJANGO_ADMIN_PASSWORD
        email = settings.DJANGO_ADMIN_EMAIL
        try:
            super_user = user.objects.create_superuser(password=password, email=email)
            um.Wallet.objects.create(created_by=super_user.id)
            return self.stdout.write(f'Super user "{email}" was created')
        except IntegrityError:
            return self.stdout.write('A user with the provided credentials already exists')
