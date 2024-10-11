import logging

from coinmarketcap_scraper import settings
from web_scraper.parsers import CryptoParser
from web_scraper import utils

logger = logging.getLogger(__name__)

 
class CoinMarketCapScraper:
    """
    Class for scraping data from CoinMarketCap.
    """

    def __init__(self, browser):
        """
        Initialize the CoinMarketCapScraper.
        ---
        Args:
            browser: The browser instance to use for scraping.
        """
        self.browser = browser

    def fetch_chunk_data(self, chunk_count, chunk_size=5):
        """
        Fetch data for a chunk of rows from the CoinMarketCap table.
        ---
        Args:
            chunk_count (int): The index of the chunk to fetch.
            chunk_size (int, optional): The number of rows in each chunk. Defaults to 5.

        Returns:
            list: A list of parsed data for the chunk.
        """
        chunk_data = []
        try:
            # Wait until the specific row in the table is present
            utils.wait_until_present(
                self.browser,
                '.cmc-table tbody tr:nth-of-type({})'.format(chunk_count * chunk_size)
            )
            table_element = self.browser.find_by_css('.cmc-table', wait_time=settings.MAXIMUM_WAIT_TIME)
            body_element = table_element.find_by_tag('tbody', wait_time=settings.MAXIMUM_WAIT_TIME)
            data_rows = body_element.find_by_tag('tr', wait_time=settings.MAXIMUM_WAIT_TIME)

            start_index = (chunk_count - 1) * chunk_size
            end_index = chunk_count * chunk_size
            parsed_data = data_rows[start_index:end_index]

            # Parse and append data for each row in the chunk
            for row_data in parsed_data:
                parser = CryptoParser(row_data)
                chunk_data.append(parser.fetch_coinmarket_data())
        except Exception as e:
            # Handle exceptions and log errors
            logger.error(f"An error occurred while fetching table data: {e}")
        return chunk_data

    def fetch_table_data(self, page_count=2, total_chunks=20):
        """
        Fetch data from multiple pages of the CoinMarketCap table.
        ---
        Args:
            page_count (int, optional): The number of pages to fetch data from. Defaults to 3.
            total_chunks (int, optional): The total number of chunks to fetch from each page. Defaults to 20.
        ---
        Returns:
            list: A list of parsed data from the table.
        """
        table_data = []
        if self.browser:
            for page_num in range(1, page_count + 1):
                # Visit the next page
                self.browser.visit(f'{settings.WEBSITE_URL}?page={page_num}')
                scroll_step = 500
                page_height = 0
                chunk_count = 1
                while chunk_count <= total_chunks:
                    # Fetch data for each chunk on the current page
                    table_data.extend(self.fetch_chunk_data(chunk_count))
                    updated_height = page_height + scroll_step
                    # Scroll to load more data
                    self.browser.execute_script(
                        f'window.scrollTo({page_height}, {updated_height});'
                    )
                    page_height = updated_height
                    chunk_count += 1

                # Break if reached the specified page count
                if page_num >= page_count:
                    break
        return table_data
