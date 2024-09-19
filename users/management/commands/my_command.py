from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'This is a custom Django command'

    def handle(self, *args, **kwargs):
        self.stdout.write('Hello from the bayan command!')
