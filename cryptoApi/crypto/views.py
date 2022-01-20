from django.shortcuts import render
from rest_framework import generics
import requests
from .models import Currency
from .serializers import CurrencySerializer
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
    print(imageURL)
    context = {
        'currency':currency,
        'imageURL':imageURL
    }
    return render(request, 'crypto/currency_page.html', context)

class CurrencyAPIView(generics.ListAPIView):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer
