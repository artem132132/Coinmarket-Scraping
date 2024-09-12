import logging
import json
import requests

from coinmarketcap_scraper import settings
from web_scraper import driver, scraper

logger = logging.getLogger(__name__)


def wait_until_present(browser, value):
    """
    Wait until the element identified by the specified CSS selector is present in the DOM.
    ---
    Args:
        browser (Splinter.browser): The Splinter browser instance.
        value (str): CSS selector to identify the target element.
    ---
    Returns:
        Splinter.element_list.ElementList or None: The first matching element if found, else None.
    """
    try:
        element = browser.find_by_css(value, wait_time=settings.MAXIMUM_WAIT_TIME)
        if element:
            return element.first
        else:
            logging.error("Element not found.")
    except Exception as e:
        logging.error(f"An error occurred while waiting for the element: {str(e)}.")

def get_text_from_element(row_element, css_selector, index=None):
    """
    Get text content from a specific element within a row element.
    ---
    Args:
        row_element (Splinter.element_list.Element): The parent element containing the target element.
        css_selector (str): CSS selector to identify the target element within the row element.
        index (int, optional): Index of the target element if multiple elements match the selector (default is None).
    ---
    Returns:
        str: Text content of the target element, or None if the element is not found.
    """
    try:
        target_element = row_element.find_by_css(css_selector, wait_time=settings.MAXIMUM_WAIT_TIME)
        if index is not None:
            target_element = target_element.find_by_tag("p", wait_time=settings.MAXIMUM_WAIT_TIME)[index]
        return target_element.text
    except Exception as e:
        logging.error(f"An error occurred while getting text from the element: {str(e)}.")

def get_src_from_element(row_element, css_selector):
    try:
        target_element = row_element.find_by_css(css_selector, wait_time=settings.MAXIMUM_WAIT_TIME)
        # print(target_element)
        # print(css_selector)
        # import pdb
        # pdb.set_trace()
        return target_element.find_by_tag("img", wait_time=settings.MAXIMUM_WAIT_TIME)['src']
    except Exception as e:
        logging.error(f"An error occurred while getting text from the element: {str(e)}.")

def scrape_coinmarket_data():
    """
    Scrapes data from CoinMarketCap using a web scraper.
    ---
    Returns:
        dict: Scraped data from CoinMarketCap.
    """
    # Initialize the web driver and scraper
    web_driver_obj = driver.DriverManager()
    web_scraper_obj = scraper.CoinMarketCapScraper(web_driver_obj.web_driver)
    
    # Fetch data from CoinMarketCap
    crypto_scrapped_data = web_scraper_obj.fetch_table_data()
    
    # Quit the web driver to release resources
    web_driver_obj.quit_web_driver()
    return crypto_scrapped_data

def post_data_to_api(data, api_url):
    """
    Posts the scraped data to the API endpoint.
    ---    
    Args:
        data (dict): Data to be posted to the API.
    ---
    Returns:
        requests.Response: Response object from the API.
    """
    # Convert data to JSON payload
    payload = json.dumps({'crypto_currencies': data})
    # Send POST request to the API, with timeout of 10 seconds
    response = requests.post(url=api_url, data=payload, headers={'Content-Type': 'application/json'}, timeout=10)
    return response
