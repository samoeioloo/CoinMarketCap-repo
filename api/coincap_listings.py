import json
import requests
import config

listing_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'

request = requests.get(listing_url,
    headers={
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': config.api_key
    }
    )
results = request.json()
# print(json.dumps(results, sort_keys = True, indent = 4))

data = results['data']

for currency in data:
    rank = currency['cmc_rank']
    symbol = currency['symbol']
    id = currency['id']
    name = currency['name']
    print(str(rank) + ': ' + name + ' (' + symbol + ')')
