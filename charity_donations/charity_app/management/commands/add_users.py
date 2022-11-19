from django.core.management.base import BaseCommand

from ._private import add_users


class Command(BaseCommand):
    help = "add users"

    def handle(self, *args, **options):
        add_users()
        self.stdout.write(self.style.SUCCESS("Successfully add users"))
