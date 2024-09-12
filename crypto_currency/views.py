from rest_framework import generics as rest_generics

from crypto_currency import (
    serializers as crypto_currency_serializers,
    models as crypto_currency_models,
    mixins as crypto_currency_mixins,
)


class CryptoCurrencyListCreateView(
    crypto_currency_mixins.MultiSerializerClassViewMixin,
    rest_generics.ListCreateAPIView,
):
    """
    API view for listing and creating CryptoCurrency objects.
    ---
    - GET method returns a list of CryptoCurrency objects.
    - POST method creates new CryptoCurrency objects in bulk.
    """
    queryset = crypto_currency_models.CryptoCurrency.objects.order_by('currency_name')

    serializer_classes = {
        'GET': crypto_currency_serializers.CryptoCurrencySerializer,
        'POST': crypto_currency_serializers.CryptoCurrencyBulkCreateSerializer,
    }
