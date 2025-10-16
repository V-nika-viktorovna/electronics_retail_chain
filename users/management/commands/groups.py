from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Добавление групп пользователей в базу данных'

    def handle(self, *args, **kwargs):

        groups = [
            {'name': 'moders'}
        ]

        for groups_data in groups:
            group, created = Group.objects.get_or_create(**groups_data)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Группа {group.name} добавлена'))
            else:
                self.stdout.write(self.style.WARNING(f'Группа {group.name} уже существует'))
