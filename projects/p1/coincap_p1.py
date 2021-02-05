import os
import json
import requests
import config
from datetime import datetime
from prettytable import PrettyTable
from colorama import init, Fore, Back, Style
init(convert=True)
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
print("MY PORTFOLIO")
print()

portfolio_value = 0.00
last_updated = None

table = PrettyTable(['Asset', 'Amount Owned', convert + ' Value', 'Price', '1h', '24h', '7d', '30d'])

with open("portfolio.txt") as inp: #stores data of file in var inp
    for line in inp:
        ticker, amount = line.split() #splits each line where there is a spacebar. first half is stored in ticker var and second half is stored in amount var
        ticker = ticker.upper()

        #ticker_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest' + str(ticker_url_pairs[ticker]) + '/' + url_end
        ticker_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?id=' + str(ticker_url_pairs[ticker])  + url_end
        request = requests.get(ticker_url, headers={
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': config.api_key
            })
        results = request.json()
        #print(ticker_url_pairs[ticker])
    #    print(json.dumps(results, sort_keys=True, indent=4))

        currency = results['data'][str(ticker_url_pairs[ticker])]

        rank = currency['cmc_rank']
        name = currency['name']
        symbol = currency['symbol']
        # dateAdded = currency['date_added']

        num_market_pairs = currency['num_market_pairs']

        quote = currency['quote'][convert]
        # market_cap = quote['market_cap']
        hour_change = quote['percent_change_1h']
        day_change = quote['percent_change_24h']
        week_change = quote['percent_change_7d']
        month_change = quote['percent_change_30d']
        price = quote['price']
        last_updated = quote['last_updated']
#        volume = quote['volume_24h']

        value = float(price) * float(amount)#calculates value of each individual asset

        if hour_change > 0:
            hour_change = Back.GREEN + str("{:.2f}".format(hour_change)) + '%' + Style.RESET_ALL
        else:
            hour_change = Back.RED + str("{:.2f}".format(hour_change)) + '%' + Style.RESET_ALL
        if day_change > 0:
            day_change = Back.GREEN + str("{:.2f}".format(day_change))  + '%' + Style.RESET_ALL
        else:
            day_change = Back.RED + str("{:.2f}".format(day_change)) + '%' + Style.RESET_ALL
        if week_change > 0:
            week_change = Back.GREEN + str("{:.2f}".format(week_change))+ '%' + Style.RESET_ALL
        else:
            week_change = Back.RED + str("{:.2f}".format(week_change)) + '%' + Style.RESET_ALL
        if month_change > 0:
            month_change = Back.GREEN + str("{:.2f}".format(month_change)) + '%' + Style.RESET_ALL
        else:
            month_change = Back.RED + str("{:.2f}".format(month_change))+ '%' + Style.RESET_ALL


        portfolio_value += value

        value_string = '{:,}'.format(round(value,2))

        table.add_row([name + '(' + symbol + ')',
        amount,
        'R' + value_string,
        'R' + str("{:.2f}".format(price)),
        str(hour_change),
        str(day_change),
        str(week_change),
        str(month_change)])

print(table)
print()

portfolio_value_string = '{:,}'.format(round(portfolio_value,2))
date_format = "%Y-%m-%dT%H:%M:%S.%fZ"
last_updated_dtObject = datetime.strptime(last_updated, date_format)
last_updated_string = last_updated_dtObject.strftime("%B %d, %Y at %H:%M:%S")
# last_updated_dtObject = datetime.strptime(last_updated, "%Y-%m-%dT%H:%M:%S")
# last_updated_string = last_updated_dtObject.strftime("%m/%d/%Y %H:%M:%S")
print("Total Portfolio Value: " + Back.GREEN + 'R' +  portfolio_value_string + Style.RESET_ALL)
print()
print("API Results Last Updated on " + last_updated_string) #API updates every 5mins
