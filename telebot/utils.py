import requests
import json
from config import keys

class ConvertionExeption(Exception):
    pass


class CryptoConverter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        if quote == base:
            raise ConvertionExeption(f'Нельзя переводить одну и туже валюту  {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionExeption('Не удалось обработать валюту')
        try:
            base_ticker = keys[base]
        except KeyError:
            raise ConvertionExeption('Не удалось обработать валюту')
        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionExeption(f'неверное значение {amount} ')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = json.loads(r.content)[keys[base]]
        return total_base