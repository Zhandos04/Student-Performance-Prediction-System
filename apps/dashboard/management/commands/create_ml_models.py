from django.core.management.base import BaseCommand
from apps.dashboard.ml_models.train_models import train_models

class Command(BaseCommand):
    help = 'Trains machine learning models for student performance prediction'

    def handle(self, *args, **kwargs):
        self.stdout.write('Training machine learning models...')
        
        try:
            train_models()
            self.stdout.write(self.style.SUCCESS('Successfully trained models!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error training models: {e}'))