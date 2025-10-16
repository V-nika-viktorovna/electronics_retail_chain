import os

from django.core.management import BaseCommand
from dotenv import load_dotenv

from users.models import User

load_dotenv(override=True)


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        user_email = os.getenv('USER_EMAIL')
        user = User.objects.create(email=user_email)
        user_pass = os.getenv('USER_PASS')
        user.set_password(user_pass)
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save()
