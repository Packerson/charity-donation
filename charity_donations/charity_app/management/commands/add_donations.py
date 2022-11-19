from django.core.management.base import BaseCommand

from ._private import add_donation


class Command(BaseCommand):
    help = "add donations"

    def handle(self, *args, **options):
        add_donation()
        self.stdout.write(self.style.SUCCESS("Successfully add donations"))
