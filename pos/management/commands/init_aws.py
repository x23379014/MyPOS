"""
Django management command to initialize AWS resources
Run: python manage.py init_aws
"""

from django.core.management.base import BaseCommand
from pos.aws_services import DynamoDBService, S3Service, SNSService
from error_handler.error_handler import ErrorHandler


class Command(BaseCommand):
    help = 'Initialize AWS resources (DynamoDB tables, S3 bucket, SNS topic)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Initializing AWS resources...'))
        
        # Create DynamoDB tables
        try:
            self.stdout.write('Creating DynamoDB tables...')
            DynamoDBService.create_tables()
            self.stdout.write(self.style.SUCCESS('✓ DynamoDB tables created/verified'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Error creating DynamoDB tables: {str(e)}'))
        
        # Create S3 bucket
        try:
            self.stdout.write('Creating S3 bucket...')
            S3Service.create_bucket()
            self.stdout.write(self.style.SUCCESS('✓ S3 bucket created/verified'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Error creating S3 bucket: {str(e)}'))
            self.stdout.write(self.style.WARNING('Note: S3 bucket names must be globally unique. You may need to change S3_BUCKET_NAME in settings.py'))
        
        # Create SNS topic
        try:
            self.stdout.write('Creating SNS topic...')
            topic_arn = SNSService.get_or_create_topic()
            self.stdout.write(self.style.SUCCESS(f'✓ SNS topic created/verified: {topic_arn}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'✗ Error creating SNS topic: {str(e)}'))
        
        self.stdout.write(self.style.SUCCESS('\nAWS resources initialization complete!'))

