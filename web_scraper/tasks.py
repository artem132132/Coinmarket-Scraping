import os
import logging

from coinmarketcap_scraper.celery import app
from web_scraper import utils

logger = logging.getLogger(__name__)


@app.task
def scrape_coinmarket_data_and_post():
    """
    Celery task to scrape CoinMarketCap data and post it to the API.
    """
    try:
        scraped_data = utils.scrape_coinmarket_data()
        utils.post_data_to_api(scraped_data, os.environ.get('CRYPTO_CURRENCY_API_ENDPOINT'))
    except Exception as e:
        logger.exception(f"Exception occurred during scraping and posting data to API {e}")
