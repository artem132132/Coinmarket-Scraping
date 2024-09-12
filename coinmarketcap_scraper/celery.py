import os
from celery import Celery

from coinmarketcap_scraper import schedules

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'coinmarketcap_scraper.settings')

app = Celery('coinmarketcap_scraper')

# Configure Celery app settings
app.conf.update(
    broker_url=os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379'),
    result_backend=os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/'),
    task_serializer='json',
    accept_content=['application/json'],
    result_serializer='json',
    timezone='UTC',
    beat_scheduler=os.environ.get('CELERY_BEAT_SCHEDULER', 'django_celery_beat.schedulers:DatabaseScheduler')
)

# Define the beat schedule
app.conf.beat_schedule = schedules.CELERY_BEAT_SCHEDULE

# Autodiscover and register tasks from all installed apps
app.autodiscover_tasks()
