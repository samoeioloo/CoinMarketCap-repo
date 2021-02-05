# Alerts user when cryptocurrency currency hits a certain target
# Samoei Oloo
# 04 Feb 2021

import os
import json
import requests
import config
from datetime import datetime
import time #allows us to wait 5 mins before making next API call
from win32com.client import Dispatch




#init(convert=True)
convert = 'ZAR'

listings_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
url_end = '&convert=' + convert

request = requests.get(listings_url, headers={
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': config.api_key
    })
results = request.json()
data=results['data']

ticker_url_pairs = {}
for currency in data:
    symbol = currency['symbol']
    url = currency['id']
    ticker_url_pairs[symbol] = url

print()
print("ALERTS TRACKING...")
print()

already_hit_symbols = [] #array that stores tickers that have already hit the target so that it is not constantly last_updated_string

while True:
    with open("alerts.txt") as inp:
        for line in inp:
            ticker, amount = line.split()
            ticker = ticker.upper()
            ticker_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?id=' + str(ticker_url_pairs[ticker])  + url_end
            request = requests.get(ticker_url, headers={
                'Accepts': 'application/json',
                'X-CMC_PRO_API_KEY': config.api_key
                })
            results = request.json()

            currency = results['data'][str(ticker_url_pairs[ticker])]
            name = currency['name']
            last_updated = currency['last_updated']
            symbol = currency['symbol']
            quote = currency['quote'][convert]
            price = quote['price']

            # if price of current cryptocurrency > alerts set, then trigger alert
            if float(price) >= float(amount) and symbol not in already_hit_symbols:
                 #os.system('say ' + name + ' hit ' + amount)
                speak = Dispatch("SAPI.SpVoice")
                speak.Speak( name + ' hit ' + amount)
                date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
                last_updated_dtObject = datetime.strptime(last_updated, date_format)
                last_updated_string = last_updated_dtObject.strftime("%B %d, %Y at %H:%M:%S")
                print(name + ' hit ' + amount + ' on ' + last_updated_string)
                already_hit_symbols.append(symbol)

    print("...")
    time.sleep(300)
