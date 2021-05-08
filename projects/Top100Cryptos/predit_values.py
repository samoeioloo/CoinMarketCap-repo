# application that sorts top 100 cryptocurrency by rank, 24h price change, 24h volume
# Samoei Oloo
# 04 Feb 2021

import os
import json
import requests
import config
from datetime import datetime
from prettytable import PrettyTable
from colorama import init, Fore, Back, Style
init(convert=True)

convert = 'ZAR'

global_url='https://pro-api.coinmarketcap.com/v1/global-metrics/quotes/latest?convert=' + convert

request = requests.get(global_url,
headers={
'Accepts': 'application/json',
'X-CMC_PRO_API_KEY': config.api_key
}
)
results = request.json()
data = results['data']

global_cap = int(data['quote'][convert]['total_market_cap'])
global_cap_string = '{:,}'.format(global_cap)

while True:

    print()
    print("CoinMarketCap Explorer Menu")
    print("The global market cap is R" + global_cap_string)
    print()
    print("1 - Top 100 sorted by rank")
    print("2 - Top 100 sorted by 24 hour change")
    print("3 - Top 100 sorted by 24 hour volume")
    print("0 - Exit")
    print()
    choice = input("What is your choice? (0-3)")

    # base url manipulated according to user choice
    ticker_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?convert=' + convert

    if choice == '1':
        ticker_url += ''
    if choice == '2':
        ticker_url += '&sort=percent_change_24h'
    if choice == '3':
        ticker_url += '&sort=volume_24h'
    if choice == '0':
        break

    request = requests.get(ticker_url, headers={
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': config.api_key
        })
    results = request.json()
    data = results['data']

    table = PrettyTable(['Rank', 'Asset', 'Price', 'Market Cap', 'Volume', '1h', '24h', '7d', '30d'])

    print()
    for currency in data:
        rank = currency['cmc_rank']
        name = currency['name']
        symbol = currency['symbol']
        quote = currency['quote'][convert]
        market_cap = quote['market_cap']
        hour_change = quote['percent_change_1h']
        day_change = quote['percent_change_24h']
        week_change = quote['percent_change_7d']
        month_change = quote['percent_change_30d']
        price = quote['price']
        volume = quote['volume_24h']

        if hour_change is not None:
            if hour_change > 0:
                hour_change = Back.GREEN + str("{:.2f}".format(hour_change)) + '%' + Style.RESET_ALL
            else:
                hour_change = Back.RED + str("{:.2f}".format(hour_change)) + '%' + Style.RESET_ALL
        if day_change is not None:
            if day_change > 0:
                day_change = Back.GREEN + str("{:.2f}".format(day_change)) + '%' + Style.RESET_ALL
            else:
                day_change = Back.RED + str("{:.2f}".format(day_change)) + '%' + Style.RESET_ALL
        if week_change is not None:
            if week_change > 0:
                week_change = Back.GREEN + str("{:.2f}".format(week_change)) + '%' + Style.RESET_ALL
            else:
                week_change = Back.RED + str("{:.2f}".format(week_change)) + '%' + Style.RESET_ALL
        if month_change is not None:
            if month_change > 0:
                month_change = Back.GREEN + str("{:.2f}".format(month_change)) + '%' + Style.RESET_ALL
            else:
                month_change = Back.RED + str("{:.2f}".format(month_change)) + '%' + Style.RESET_ALL

        if volume is not None:
            volume_string = '{:.2f}'.format(volume)
            #volume_string = "{:.2f}".format(volume_string)

        if market_cap is not None:
            market_cap_string = "{:,}".format(market_cap)
#            market_cap_string = "{:.2f}".format(market_cap_string)

        table.add_row([rank,
                    name + ' (' + symbol + ')',
                    'R' + str("{:.2f}".format(price)),
                    'R' + str("{:.2f}".format(market_cap)),
                    'R' + volume_string,
                    str(hour_change),
                    str(day_change),
                    str(week_change),
                    str(month_change)])

    print()
    print(table)
    print()

    choice = input("Again? (y/n): ")

    if choice == 'n':
        break
