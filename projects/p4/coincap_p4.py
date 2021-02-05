# Application returns potential future values of cryptocurrencies
# Samoei Oloo
# 05 Feb 2021


import math
import json
import config
import locale
import requests
from prettytable import PrettyTable

convert = 'ZAR'
# set locale
locale.setlocale(locale.LC_ALL, 'en_ZA.UTF-8')
global_url='https://pro-api.coinmarketcap.com/v1/global-metrics/quotes/latest?convert=' + convert
ticker_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?convert=' + convert

request = requests.get(global_url,
    headers={
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': config.api_key
    })
results = request.json()

global_cap = results['data']['quote'][convert]['total_market_cap']

table = PrettyTable(['Name', 'Ticker', '% of total global cap', 'Current', '10.9T(Gold)', '35.2T (Narrow Money)', 'USD 89.5T (World Stock Markets)', 'USD 95.7T (Broad Money)', 'USD 280.6T (Real Estate)', 'USD 558.5T (Derivatives)'])

request = requests.get(ticker_url, headers={
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': config.api_key
    })
results = request.json()
data = results['data']

for currency in data:
    name = currency['name']
    ticker = currency['symbol']
    percentage_of_global_cap = float(currency['quote'][convert]['market_cap']) / float(global_cap)

    current_price = round(float(currency['quote'][convert]['price']), 2)
    max_supply = currency['max_supply']
    circulating_supply = currency['circulating_supply']
    # print(circulating_supply)

    if max_supply is not None and max_supply > 0:
        trillion10price = round(10900000000000 * percentage_of_global_cap / max_supply, 2)
        trillion35price = round(35200000000000 * percentage_of_global_cap / max_supply, 2)
        trillion89price = round(89500000000000 * percentage_of_global_cap / max_supply, 2)
        trillion95price = round(95700000000000 * percentage_of_global_cap / max_supply, 2)
        trillion280price = round(280600000000000 * percentage_of_global_cap / max_supply, 2)
        trillion558price = round(558500000000000 * percentage_of_global_cap / max_supply, 2)
    else:
        trillion10price = round(10900000000000 * percentage_of_global_cap / circulating_supply, 2)
        trillion35price = round(35200000000000 * percentage_of_global_cap / circulating_supply, 2)
        trillion89price = round(89500000000000 * percentage_of_global_cap / circulating_supply, 2)
        trillion95price = round(95700000000000 * percentage_of_global_cap / circulating_supply, 2)
        trillion280price = round(280600000000000 * percentage_of_global_cap / circulating_supply, 2)
        trillion558price = round(558500000000000 * percentage_of_global_cap / circulating_supply, 2)

    percentage_of_global_cap_string = str(round(percentage_of_global_cap*100,2)) + '%'
    current_price_string = 'R' + str(current_price)
    trillion10price_string = 'R' + locale.format_string('%.2f', trillion10price,True)
    trillion35price_string = 'R' + locale.format_string('%.2f', trillion35price,True)
    trillion89price_string = 'R' + locale.format_string('%.2f', trillion89price,True)
    trillion95price_string = 'R' + locale.format_string('%.2f', trillion95price,True)
    trillion280price_string = 'R' + locale.format_string('%.2f', trillion280price,True)
    trillion558price_string = 'R' + locale.format_string('%.2f', trillion558price,True)

    table.add_row([name,
                ticker,
                percentage_of_global_cap_string,
                current_price_string,
                trillion10price_string,
                trillion35price_string,
                trillion89price_string,
                trillion95price_string,
                trillion280price_string,
                trillion558price_string
                ])

print()
print(table)
print()
