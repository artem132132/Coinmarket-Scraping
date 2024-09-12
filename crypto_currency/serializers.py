from rest_framework import serializers

from crypto_currency import models as crypto_currency_models


class CryptoCurrencySerializer(serializers.ModelSerializer):
    """
    Serializer for individual crypto currency details
    """

    class Meta:
        model = crypto_currency_models.CryptoCurrency
        exclude = []


class CryptoCurrencyBulkCreateSerializer(serializers.Serializer):
    """
    Serializer for bulk create/update of crypto currency details
    """

    crypto_currencies = CryptoCurrencySerializer(many=True, write_only=True)

    def create(self, *args, **kwargs):
        """
        Create or update multiple crypto currencies in bulk
        ---
        Args:
        - kwargs: Additional keyword arguments
        """
        crypto_currencies = self.validated_data.pop('crypto_currencies', [])
        currency_names = [item.get('currency_name') for item in crypto_currencies]

        # Fetch existing crypto currencies from the database
        existing_currencies = crypto_currency_models.CryptoCurrency.objects.filter(currency_name__in=currency_names)

        # Create a dictionary of existing currencies for quick lookup
        existing_currency_dict = {crypto.currency_name: crypto for crypto in existing_currencies}

        # Lists to hold instances for bulk create/update operations
        currencies_to_update = []
        currencies_to_create = []

        for item in crypto_currencies:
            currency_name = item['currency_name']
            instance = existing_currency_dict.get(currency_name)
            if instance:
                # Update existing instance with validated data
                for attr, value in item.items():
                    setattr(instance, attr, value)
                currencies_to_update.append(instance)
            else:
                new_instance = crypto_currency_models.CryptoCurrency(**item)
                currencies_to_create.append(new_instance)

        # Perform bulk update if there are instances to update
        if currencies_to_update:
            crypto_currency_models.CryptoCurrency.objects.bulk_update(
                currencies_to_update, crypto_currency_models.CryptoCurrency.MODEL_FIELDS
            )

        # Perform bulk create if there are instances to create
        crypto_currency_models.CryptoCurrency.objects.bulk_create(currencies_to_create)
        return self.validated_data
