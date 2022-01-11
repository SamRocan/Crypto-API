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


    for i in range(len(currencies)):
        currency_obj = []
        currency = currencies[i].find_all("td")
        currency_obj.append(int(currency[0].text))
        currency_obj.append(currency[1].find("img")['src'])
        currency_obj.append(currency[1].text.split()[0])
        currency_obj.append(currency[1].text.split()[1][1:len(currency[1].text.split()[1])-1])
        currency_obj.append(int((currency[2].text).replace(',','')))
        currency_obj.append(float(currency[3].text[:len(currency[3].text)-1]))
        currency_obj.append(float(currency[4].text[1:len(currency[4].text)].replace(',','')))
        currency_obj.append(float(currency[5].text))
        print(currency_obj)

        Currency.objects.create(
            rank=currency_obj[0],
            image=currency_obj[1],
            name=currency_obj[2],
            symbol=currency_obj[3],
            market_cap=currency_obj[4],
            market_share=currency_obj[5],
            price=currency_obj[6],
            day_change=currency_obj[7]
        )
        sleep(5)

@shared_task
def update_currency():
    print("Creating crypto currency data")
    req = Request("https://www.slickcharts.com/currency", headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    soup = BeautifulSoup(html, 'html.parser')
    currencies = soup.find("tbody").find_all("tr")


    for i in range(len(currencies)):
        currency_obj = []
        currency = currencies[i].find_all("td")
        currency_obj.append(int(currency[0].text))
        currency_obj.append(currency[1].find("img")['src'])
        currency_obj.append(currency[1].text.split()[0])
        currency_obj.append(currency[1].text.split()[1][1:len(currency[1].text.split()[1])-1])
        currency_obj.append(int((currency[2].text).replace(',','')))
        currency_obj.append(float(currency[3].text[:len(currency[3].text)-1]))
        currency_obj.append(float(currency[4].text[1:len(currency[4].text)].replace(',','')))
        currency_obj.append(float(currency[5].text))
        print(currency_obj)

        Currency.objects.filter(rank=currency_obj[0]).update(
            rank=currency_obj[0],
            image=currency_obj[1],
            name=currency_obj[2],
            symbol=currency_obj[3],
            market_cap=currency_obj[4],
            market_share=currency_obj[5],
            price=currency_obj[6],
            day_change=currency_obj[7]
        )

create_currency()

while True:
    sleep(60)
    update_currency()
