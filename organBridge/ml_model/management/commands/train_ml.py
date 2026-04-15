from django.core.management.base import BaseCommand
from ml_model.train_model import MLModelTrainer


class Command(BaseCommand):
    help = 'Train the OrganBridge ML matching model'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting ML model training...')
        trainer = MLModelTrainer()
        success = trainer.train_complete_pipeline()
        if success:
            self.stdout.write(self.style.SUCCESS('ML model trained successfully!'))
        else:
            self.stdout.write(self.style.ERROR('ML model training failed!'))