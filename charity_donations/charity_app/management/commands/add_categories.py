from django.core.management.base import BaseCommand

from ._private import add_category


class Command(BaseCommand):
    help = "add categories"

    def handle(self, *args, **options):
        add_category()
        self.stdout.write(self.style.SUCCESS("Successfully add categories"))
