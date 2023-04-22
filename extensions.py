import json
import requests
from config import keys


class ConvertinException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertinException(f'Невозможно перевести одинаковые валюты {base}.')

        try:
            quote_Tiker = keys[quote]
        except KeyError:
            raise ConvertinException(f'Не удалось обработать валюту {quote}')

        try:
            base_Tiker = keys[base]
        except KeyError:
            raise ConvertinException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConvertinException(f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_Tiker}&tsyms={base_Tiker}')
        total_base = json.loads(r.content)[keys[base]]
        total_base = total_base * amount

        return total_base
