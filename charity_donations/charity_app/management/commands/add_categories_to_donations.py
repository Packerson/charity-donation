from django.core.management.base import BaseCommand

from ._private import add_categories_to_donations


class Command(BaseCommand):
    help = "add categories"

    def handle(self, *args, **options):
        add_categories_to_donations()
        self.stdout.write(self.style.SUCCESS("Successfully add categories"))
