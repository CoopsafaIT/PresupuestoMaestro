from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from apps.security.models import UserProfile


class Command(BaseCommand):
    help = "Command for CREATE user's profile"

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        counter = 0
        for user in users:
            obj, created = UserProfile.objects.get_or_create(
                user_id=user, defaults={'user_validate_ad': True}
            )
            if created:
                counter = counter + 1

        print(f'Created: {counter}')
        self.stdout.write(self.style.SUCCESS("Command execution ended Successfully!!"))
