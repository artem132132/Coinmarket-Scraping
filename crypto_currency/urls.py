from django.urls import path

from crypto_currency import views as crypto_currency_views

urlpatterns = [
    path('', crypto_currency_views.CryptoCurrencyListCreateView.as_view(), name='crypto-currencies')
]
