import json
import requests
import config
from datetime import datetime

currency = 'ZAR'

global_url = 'https://pro-api.coinmarketcap.com/v1/global-metrics/quotes/latest?convert=' + currency

request = requests.get(global_url, #gets global_url and puts json data inside request var
    headers={
    'Accepts': 'application/json',
    'X-CMC_PRO_API_KEY': config.api_key
    }
    )

#format json data
results = request.json()

#print out json data to terminal
#print(json.dumps(results, sort_keys = True, indent = 4)) #puts it in human readable format for better understanding

#store API data in variables
active_currencies = results['data']['active_cryptocurrencies']
active_exchanges = results['data']['active_exchanges']
active_market_pairs = results['data']['active_market_pairs']
btc_dominance = results['data']['btc_dominance']
defi_24h_perc_change = results['data']['defi_24h_percentage_change']
defi_market_cap = results['data']['defi_market_cap']
defi_volume = results['data']['defi_volume_24h']
defi_vol_reported = results['data']['defi_volume_24h_reported']
derivatives_24h_percentage_change = results['data']['derivatives_24h_percentage_change']
derivatives_volume_24h = results['data']['derivatives_volume_24h']
derivatives_volume_24h_reported = results['data']['derivatives_volume_24h_reported']
eth_dominance = results['data']['eth_dominance']
last_updated = results['data']['last_updated']
altcoin_market_cap = results['data']['quote'][currency]['altcoin_market_cap']
altcoin_volume_24h = results['data']['quote'][currency]['altcoin_volume_24h']
altcoin_volume_24h_reported = results['data']['quote'][currency]['altcoin_volume_24h_reported']
last_update_USD = results['data']['quote'][currency]['last_updated']
global_cap = results['data']['quote'][currency]['total_market_cap']
global_volume = results['data']['quote'][currency]['total_volume_24h']
global_volume_reported = results['data']['quote'][currency]['total_volume_24h_reported']

active_currencies_string = '{:,}'.format(active_currencies)
active_market_pairs_string = '{:,}'.format(active_market_pairs)
global_cap_string = '{:,}'.format(global_cap)
global_volume_string = '{:,}'.format(global_volume)
altcoin_market_cap_string = '{:,}'.format(altcoin_market_cap)

#last_updated_string = datetime.fromtimestamp(last_updated).strftime('%B %d, %f at %I:%M%p')

print()
print('There are currently ' + active_currencies_string + ' active cryptocurrencies and ' + active_market_pairs_string + ' active market pairs' )
print('The global cap of all cryptos is ' + global_cap_string + ' and the 24h global volume is ' + global_volume_string
 + '.')
print('Altcoin\'s market cap is ' + altcoin_market_cap_string)
print()
print('This information was last updated ' + str(last_updated))
