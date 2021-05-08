import xlsxwriter
import requests
import json
import config

convert = 'ZAR'
start = 1 #use this number to paginate through files
f = 1 #f specifies the row. start with row one and increment so it goes into each row

crypto_workbook = xlsxwriter.Workbook('cryptocurrencies.xlsx')
crypto_sheet = crypto_workbook.add_worksheet()

crypto_sheet.write('A1', 'Name')
crypto_sheet.write('B1', 'Symbol')
crypto_sheet.write('C1', 'Market Cap')
crypto_sheet.write('D1', 'Price')
crypto_sheet.write('E1', '24h Volume')
crypto_sheet.write('F1', 'Hour Change')
crypto_sheet.write('G1', 'Day Change')
crypto_sheet.write('H1', 'Week Change')
crypto_sheet.write('I1', 'Month Change')

for i in range(10):
    ticker_url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?convert=' + convert + '&start=' +str(start)

    request = requests.get(ticker_url, headers={
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': config.api_key
        })
    results = request.json()
    data = results['data']

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

        crypto_sheet.write(f,0,name) #f 0 is column 1
        crypto_sheet.write(f,1,symbol)
        crypto_sheet.write(f,2,str(market_cap))
        crypto_sheet.write(f,3,str(price))
        crypto_sheet.write(f,4,str(volume))
        crypto_sheet.write(f,5,str(hour_change))
        crypto_sheet.write(f,6,str(day_change))
        crypto_sheet.write(f,7,str(week_change))
        crypto_sheet.write(f,8,str(month_change))

        f+=1

    start +=100

crypto_workbook.close()
