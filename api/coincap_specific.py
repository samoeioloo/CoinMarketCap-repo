import requests
import json
import config

convert = 'ZAR'

listing_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
url_end = '&convert=' + convert

request = requests.get(listing_url,
    headers={
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': config.api_key
    }
    )
results = request.json()

data = results["data"]
# print(json.dumps(results, sort_keys = True, indent = 4))

ticker_url_pairs = {} #dictionary that stores ticker value as key and id as the value
for currency in data:
    symbol = currency['symbol']
    url = currency['id']
    ticker_url_pairs[symbol] = url

# print(ticker_url_pairs)

while True:

    print()
    choice = input("Enter the ticker symbol of a cryptocurrency: ")
    choice = choice.upper()

    ticker_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?id=' + str(ticker_url_pairs[choice])  + url_end

    request = requests.get(ticker_url,
        headers={
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': config.api_key
        }
        )
    results = request.json()

    # print(json.dumps(results, sort_keys=True, indent=4))

    currency = results['data'][str(ticker_url_pairs[choice])]

    # currency = list(results)
    # print(currency[0])
    #currency = results[list(results.keys())[1]]
    #
    rank = currency['cmc_rank']
    name = currency['name']
    symbol = currency['symbol']
    dateAdded = currency['date_added']
    num_market_pairs = currency['num_market_pairs']

    circulating_supply = currency['circulating_supply']
    max_supply = currency['max_supply']

    id = currency['id']
    #last_updated = currency['last_updated']

    platform = currency['platform']

    quote = currency['quote'][convert]
    market_cap = quote['market_cap']
    hour_change = quote['percent_change_1h']
    day_change = quote['percent_change_24h']
    week_change = quote['percent_change_7d']
    month_change = quote['percent_change_30d']
    price = quote['price']
    volume = quote['volume_24h']

    volume_string = '{:,}'.format(volume)
    market_cap_string = '{:,}'.format(market_cap)
    circulating_supply_string = '{:,}'.format(circulating_supply)
    #max_supply_string = '{:,}'.format(max_supply)

    print(str(rank) + ': ' + name + ' (' + symbol + ')')
    print("Market cap: \t\tR" + market_cap_string)
    print("Price: \t\t\tR" + str(price))
    print("24h Volume: \t\tR" + volume_string)
    print("Hour change: \t\t" + str(hour_change) + '%')
    print("Day change: \t\t" + str(day_change) + '%')
    print("Week change: \t\t" + str(week_change) + '%')
    print("Month change: \t\t" + str(month_change) + '%')
    print("Maximum supply: \t" + str(max_supply))
    print("Circulating supply: \t" + circulating_supply_string)
    print("Percentage of coins in circulation: " + str((circulating_supply / float(max_supply))*100))
    print()

    choice = input("Again? (y/n): ")

    if choice == 'n':
        break
