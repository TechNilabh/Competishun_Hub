from django.core.management.base import BaseCommand
from api.models import ExamSession

class Command(BaseCommand):
    help = 'Reset all exam sessions for testing'

    def handle(self, *args, **options):
        ExamSession.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('All sessions deleted!'))