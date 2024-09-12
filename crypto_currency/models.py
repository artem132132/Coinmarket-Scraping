from django.db import models


class BaseDateTimeModel(models.Model):
    """
    Abstract base class model that provides self-managed created_at and updated_at fields.
    """
    created_at = models.DateTimeField(auto_now_add=True, help_text="The datetime when the object was created.")
    updated_at = models.DateTimeField(auto_now=True, help_text="The datetime when the object was last updated.")

    class Meta:
        abstract = True


class CryptoCurrency(BaseDateTimeModel):
    """
    Model to store cryptocurrency data.
    """
    MODEL_FIELDS = [
        'currency_name', 'symbol', 'logo', 'current_price', 'hourly_change', 'daily_change',
        'weekly_change', 'market_capital', 'trade_volume_usd', 'trade_volume_crypto', 'circulating_supply'
    ]

    currency_name = models.CharField(max_length=255, help_text="The name of the cryptocurrency.")
    symbol = models.CharField(max_length=64, help_text="The symbol of the cryptocurrency.")
    logo = models.URLField(null=True, blank=True, help_text="URL of the cryptocurrency's logo.")
    current_price = models.CharField(max_length=64, help_text="The current price of the cryptocurrency.")
    hourly_change = models.CharField(max_length=64, help_text="The hourly change in the cryptocurrency's price.")
    daily_change = models.CharField(max_length=64, help_text="The daily change in the cryptocurrency's price.")
    weekly_change = models.CharField(max_length=64, help_text="The weekly change in the cryptocurrency's price.")
    market_capital = models.CharField(max_length=255, help_text="The market capitalization of the cryptocurrency.")
    trade_volume_usd = models.CharField(max_length=255, help_text="The trading volume in USD.")
    trade_volume_crypto = models.CharField(max_length=255, help_text="The trading volume in cryptocurrency.")
    circulating_supply = models.CharField(max_length=255, help_text="The circulating supply of the cryptocurrency.")
