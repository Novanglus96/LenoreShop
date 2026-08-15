from django.core.management.base import BaseCommand
from django.core.management import call_command
from api.models import Store


class Command(BaseCommand):
    help = "Load demo stores, aisles, items, and shopping lists (only runs on an empty database)"

    def handle(self, *args, **options):
        if Store.objects.exists():
            self.stdout.write(self.style.WARNING(
                "Demo data not loaded: stores already exist. "
                "Clear all stores first if you want to reset to demo data."
            ))
            return

        call_command("loaddata", "demo_data")
        self.stdout.write(self.style.SUCCESS(
            "Demo data loaded: 2 stores, aisles, items, and starter shopping lists."
        ))
