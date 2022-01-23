from django.shortcuts import render
from rest_framework import generics
import requests
from .models import Currency
from .serializers import CurrencySerializer
from .rss import getNews
from django.templatetags.static import static

# Create your views here.
def index(request):
    currencies = Currency.objects.all()
    context = {
        'currencies':currencies,
    }
    return render(request, 'crypto/index.html', context)

def currency_page(request, symbol):
    currency = Currency.objects.get(symbol=symbol)

    imageURL = static('images/'+symbol+'.png')
    news = getNews(currency.name)
    print(imageURL)
    graphURL = "https://widget.coinlib.io/widget?type=chart&theme=light&coin_id=" + str(currency.coinlib_id) + "&pref_coin_id=1505"
    print(graphURL)
    context = {
        'currency':currency,
        'imageURL':imageURL,
        'graphURL':graphURL,
        'news':news
    }
    return render(request, 'crypto/currency_page.html', context)

class CurrencyAPIView(generics.ListAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
