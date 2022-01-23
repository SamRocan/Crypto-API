from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

def getNews(query):
    url = "https://news.google.com/rss/search?q="+query+"&hl=en-GB&gl=GB&ceid=GB:en"
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(req).read()
    soup = BeautifulSoup(html, 'html.parser')
    articles = soup.findAll("item")
    titles = []
    links = []
    for i in articles:
        titles.append(i.find("title").text)
        start = str(i).find('<link/>') +7
        finish = str(i).find('<guid')
        links.append(str(i)[start:finish])
    return zip(titles, links)