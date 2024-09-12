import logging

from selenium import webdriver
from splinter import Browser

logger = logging.getLogger(__name__)


class DriverManager:
    """
    A class to manage Splinter WebDriver instances.
    """

    def __init__(self):
        """
        Initializes the DriverManager with the specified URL.
        """
        self.web_driver = None
        self._initialize_web_driver()

    def _initialize_web_driver(self):
        """
        Initializes the Splinter WebDriver instance with optional query parameters.
        ---
        Args:
            query_params (str, optional): Query parameters to append to the URL.
        Raises:
            Exception: If an error occurs while initializing the WebDriver instance.
        """
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--start-maximized')

        try:
            self.web_driver = Browser(driver_name='chrome', options=options)
        except Exception as e:
            raise Exception(f"Error initializing WebDriver instance: {e}")

    def quit_web_driver(self):
        """
        Quits the Splinter WebDriver instance.
        ---
        Raises:
            Exception: If an error occurs while quitting the WebDriver instance.
        """
        try:
            if self.web_driver:
                self.web_driver.quit()
        except Exception as e:
            raise Exception(f"Error quitting WebDriver instance: {e}")
