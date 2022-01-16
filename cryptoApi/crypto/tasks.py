from time import sleep
from celery import shared_task
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
from .models import Currency

# to run worker
# celery -A cryptoApi worker --loglevel=info

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

        '''currency_obj.append(int(currency[0].text))
        currency_obj.append(currency[1].find("img")['src'])
        currency_obj.append(currency[1].text.split()[0])
        currency_obj.append(currency[1].text.split()[1][1:len(currency[1].text.split()[1])-1])
        currency_obj.append(int((currency[2].text).replace(',','')))
        currency_obj.append(float(currency[3].text[:len(currency[3].text)-1]))
        currency_obj.append(float(currency[4].text[1:len(currency[4].text)].replace(',','')))
        currency_obj.append(float(currency[5].text))
        print(currency_obj)'''

        Currency.objects.create(
            rank=rank,
            image=image,
            name=name,
            symbol=symbol,
            market_cap=market_cap,
            market_share=market_share,
            price=price,
            day_change=day_change
        )
        sleep(5)

@shared_task
def update_currency():
    print("Creating crypto currency data")
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

        data = {'rank':rank, 'image':image, 'name':name, 'symbol':symbol, 'market_cap':market_cap, 'market_share':market_share, 'price':price, 'day_change':day_change}

        Currency.objects.filter(rank=rank).update(**data)

create_currency()

while True:
    sleep(60)
    update_currency()
