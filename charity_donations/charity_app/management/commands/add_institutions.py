from django.core.management.base import BaseCommand

from ._private import add_institution


class Command(BaseCommand):
    help = "add institutions"

    def handle(self, *args, **options):
        add_institution()
        self.stdout.write(self.style.SUCCESS("Successfully add institutions"))
