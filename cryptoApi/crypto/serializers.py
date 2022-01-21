from rest_framework import serializers
from .models import Currency

class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['rank', 'name', 'symbol', 'market_cap', 'market_share', 'price', 'day_change']