from web_scraper import utils


class CryptoParser:
    """
    Represents data related to cryptocurrency extracted from a webpage.
    ---
    Methods:
    - is_trend_positive(trend_element): Checks if the trend is positive based on the trend indicator element.
    - get_changed_value(css_selector): Get the change value from the specified CSS selector.
    - fetch_coinmarket_data(): Fetch cryptocurrency data from the row element.
    """

    def __init__(self, row_element):
        """
        Initialize CryptoData with a row element from the webpage.
        ---
        Parameters:
        - row_element: The HTML element representing a row of cryptocurrency data.
        """
        self.row_element = row_element

    def is_trend_positive(self, trend_element):
        """
        Checks if the trend is positive based on the trend indicator element.
        ---        
        Parameters:
        - trend_element: The HTML element containing the trend indicator.
        ---
        Returns:
        - True if the trend is positive, False otherwise.
        """
        trend_indicator = trend_element.find_by_css("span > span")
        return "icon-Caret-up" in trend_indicator["class"]

    def get_changed_value(self, css_selector):
        """
        Get the change value from the specified CSS selector.
        ---
        Parameters:
        - css_selector: The CSS selector to locate the change element.
        ---
        Returns:
        - The changed value as a string.
        """
        change_element = self.row_element.find_by_css(css_selector)
        change_value = utils.get_text_from_element(self.row_element, css_selector)
        return f"-{change_value}" if not self.is_trend_positive(change_element) else change_value

    def fetch_coinmarket_data(self):
        """
        Fetch cryptocurrency data from the row element using there element identifiers.
        ---
        Returns:
        - A dictionary containing cryptocurrency data.
        """
        return {
            "currency_name": utils.get_text_from_element(self.row_element, "td:nth-of-type(3)", 0),
            "symbol": utils.get_text_from_element(self.row_element, "td:nth-of-type(3)", 1),
            "logo": utils.get_src_from_element(self.row_element, "td:nth-of-type(3)"),
            "current_price": utils.get_text_from_element(self.row_element, "td:nth-of-type(4)"),
            "hourly_change": self.get_changed_value("td:nth-of-type(5)"),
            "daily_change": self.get_changed_value("td:nth-of-type(6)"),
            "weekly_change": self.get_changed_value("td:nth-of-type(7)"),
            "market_capital": utils.get_text_from_element(self.row_element, "td:nth-of-type(8)"),
            "trade_volume_usd": utils.get_text_from_element(self.row_element, "td:nth-of-type(9)", 0),
            "trade_volume_crypto": utils.get_text_from_element(self.row_element, "td:nth-of-type(9)", 1),
            "circulating_supply": utils.get_text_from_element(self.row_element, "td:nth-of-type(10)"),
        }
