from bs4 import BeautifulSoup, Tag

import requests
from requests import Response


def get_stock_current_price(stock_short_name):
    url = r"https://www.set.or.th/th/market/product/stock/quote/" + \
        stock_short_name + r"/financial-statement/company-highlights"

    res: Response = requests.get(url=url)
    soup = BeautifulSoup(res.text, 'html.parser')

    # current_price = ''
    for D in soup.find_all('div', class_="quote-info"):
        D: Tag

        for div2 in D.find_all('div', class_="quote-info-left-values"):
            div2: Tag
            for h1 in div2.find_all('h1'):
                h1: Tag
                return h1.text.strip()


def get_finance_statement(stock_short_name):
    url = r"https://www.set.or.th/th/market/product/stock/quote/" + \
        stock_short_name + r"/financial-statement/company-highlights"

    url = r"https://www.set.or.th/api/set/stock/" + \
        stock_short_name + "/company-highlight/financial-data?lang=th"

    res: Response = requests.get(url=url, params={
        'lang': 'th'
    })
    print(res.json)
    # soup = BeautifulSoup(res.text, 'html.parser')

    # for i, table in enumerate(soup.find_all('table')):
    #     table: Tag
    #     for thead in table.find_all('thead'):
    #         print(thead)
    #     #     for tr in thead.find_all('tr'):
    #     #         pass


if __name__ == "__main__":
    import json

    url = r"https://pokeapi.co/api/v2/pokemon/ditto"
    url = r"https://pokeapi.co/api/v2/pokemon/PKMNID/"
    res: Response = requests.get(url=url)

    data = res.json()

    print(type(data))
    # get_finance_statement('AIT')
    # stocks = ['AIT', 'SCC', 'IRPC', 'GC', 'GIT', 'TISCO']
    # for stock in stocks:
    #     current_price = get_stock_current_price(stock)
    #     print('Stock:', stock, current_price)

    #     for h1 in div.find_all('h1'):
    #         print(' h1:', h1)

    # soup = BeautifulSoup('<b class="boldest">Extremely bold</b>', 'html.parser')
