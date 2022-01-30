from datetime import datetime, timezone
from time import sleep
from celery import shared_task
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from .models import Currency

COIN_IDS = {
    'BTC':859,
    'ETH':145,
    'USDT':637,
    'BNB':1209,
    'OI':648685,
    'ADA':122882,
    'XRP':619,
    'SOL':859, #graph not found
    'LUNA':1511102,
    'DOGE':280,
    'DOT':250,
    'AVAX':1512453,
    'BUSD':1511323,
    'SHIB':859, #graph not found
    'UST':859, #graph not found
    'MATIC':1510954,
    'ATOM':392,
    'WBTC':859,#graph not found
    'DAI':345508,
    'CRO':1510617,
}


def matchCoinLib(symbol):
    if(symbol in COIN_IDS.keys()):
        return COIN_IDS[symbol]
    return 859

# to run worker
# celery -A cryptoApi worker --loglevel=info
# or
# celery -A cryptoApi worker -l info
# or
# celery -A cryptoApi beat -l info
@shared_task
def create_currency():
    print("Creating crypto currency data")
    req = Request("https://www.slickcharts.com/currency", headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    soup = BeautifulSoup(html, 'html.parser')
    currencies = soup.find("tbody").find_all("tr")


    for i in range(10): #change to len(currencies) to get all
        currency_obj = []
        currency = currencies[i].find_all("td")
        print(currency)
        rank = int(currency[0].text)
        image = currency[1].find("img")['src']
        name = currency[1].text.split()[0]
        symbol = currency[1].text.split()[1][1:len(currency[1].text.split()[1])-1]
        market_cap = int((currency[2].text).replace(',',''))
        market_share = float(currency[3].text[:len(currency[3].text)-1])
        price = float(currency[4].text[1:len(currency[4].text)].replace(',',''))
        day_change = float(currency[5].text)
        coinlib_id = matchCoinLib(symbol)


        Currency.objects.create(
            rank=rank,
            image=image,
            name=name,
            symbol=symbol,
            market_cap=market_cap,
            market_share=market_share,
            price=price,
            day_change=day_change,
            coinlib_id=coinlib_id
        )
        sleep(5)
    print("Data Created")


@shared_task
def update_currency():
    print("Updating crypto currency data")
    req = Request("https://www.slickcharts.com/currency", headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    soup = BeautifulSoup(html, 'html.parser')
    currencies = soup.find("tbody").find_all("tr")


    for i in range(10): #change to len(currencies) to get all
        currency_obj = []
        currency = currencies[i].find_all("td")
        rank = int(currency[0].text)
        image = currency[1].find("img")['src']
        name = currency[1].text.split()[0]
        symbol = currency[1].text.split()[1][1:len(currency[1].text.split()[1])-1]
        market_cap = int((currency[2].text).replace(',',''))
        market_share = float(currency[3].text[:len(currency[3].text)-1])
        price = float(currency[4].text[1:len(currency[4].text)].replace(',',''))
        day_change = float(currency[5].text)
        coinlib_id = matchCoinLib(symbol)
        last_updated = datetime.now(tz=timezone.utc)

        data = {'rank':rank, 'image':image, 'name':name, 'symbol':symbol, 'market_cap':market_cap, 'market_share':market_share, 'price':price, 'day_change':day_change, 'coinlib_id':coinlib_id, 'last_updated':last_updated}
        print(data)
        Currency.objects.filter(rank=rank).update(**data)

if(len(Currency.objects.all()) != 10):
    create_currency()
print(len(Currency.objects.all()))

while True:
    sleep(60)
    update_currency()
