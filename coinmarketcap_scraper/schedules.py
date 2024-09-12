from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    "coinmarketcap_data_scrapper_task": {
        "task": "web_scraper.tasks.scrape_coinmarket_data_and_post",
        "schedule": 8, # Runs every 12 seconds
        "description": "Task to scrape data from coinmarket every 20 seconds",
    },
}
