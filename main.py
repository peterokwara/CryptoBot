import time
import requests
import hashlib
import hmac

# Seconds
TICK_INTERVAL = 60

# Api key from bittrex
API_KEY = '10b5d58a665b4b86b44b05e54b276ad3'
API_SECRET_KEY = b'63a7b7ae598c40689e23d07f1a7e6e80'

def main():
    print('Starting trader bot, ticking every ' + str(TICK_INTERVAL) + ' seconds')

    while True:
        start = time.time()
        tick()
        end = time.time()

        # Sleep the thread if needed
        if end - start < TICK_INTERVAL:
            time.sleep(TICK_INTERVAL - (end - start))

def tick():
    print('Running routine')
    market_summaries = simple_request('https://bittrex.com/api/v1.1/public/getmarketsummaries')
    for summary in market_summaries['result']:
        market = summary['MarketName']
        day_close = summary['PrevDay']
        last = summary['Last']

        percent_chg = ((last / day_close) - 1) * 100
        print(market + ' changed ' + str(percent_chg))

        if 40 < percent_chg < 60:
            print('Purchasing 5 units of' + market + 'for' + str(format_float(last)))
            res = buy_limit(market, 5, last)
            print(res)

        if percent_chg < -20:
            #Ship is sinking,  get out
            sell_limit(market, 5, last)

def buy_limit(market, quantity, rate):
    url = 'https://bittrex.com/api/v1.1/market/buylimit?apikey=' + API_KEY + '&market=' + market + '&quantity=' + str(quantity) + '&rate=' + format_float(rate)
    return signed_request(url)

def sell_limit(market, quantity, rate):
    url = 'https://bittrex.com/api/v1.1/market/selllimit?apikey=' + API_KEY + '&market=' + market + '&quantity=' + str(quantity) + '&rate=' + format_float(rate)
    return signed_request(url)

def signed_request(url):
    now = time.time()
    url += '&nonce=' + str(now)
    signed = hmac.new(API_SECRET_KEY, url.encode('utf-8'), hashlib.sha512).hexdigest()
    headers = {'apisign': signed}
    r = requests.get(url, headers=headers)
    return r.json()

def simple_request(url):
    r = requests.get(url)
    return r.json()

def format_float(f):
    return "%.8f" % f

if __name__ == "__main__":
    main()
