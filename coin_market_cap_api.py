import requests
import json


def price_of_crypt(crypto, currency):
    """функция возвращающая цену любой криптовалюты (crypto) в валюте (currency)"""
    try:
        crypto = crypto.lower()
        currency = currency.upper()

        url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
        parameters = {
            'slug': f'{crypto}',
            'convert': f'{currency}'
        }
        headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': '881ca7de-a5a6-4971-885a-3d800be10159',
        }

        session = requests.Session()
        session.headers.update(headers)

        response = session.get(url, params=parameters)
        data = json.loads(response.text)
        for k in data["data"]:
            id = k
            print(k)
        price = data["data"][f"{id}"]["quote"][f'{currency}']["price"]
        return price
    except Exception as e:
        print(e)
