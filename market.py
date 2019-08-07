# -----------------------------------------------------------------------------

import configparser
import datetime
import json
import time
from pprint import pprint

import ccxt

# -----------------------------------------------------------------------------
from heiken_ashi import heiken_ashi

config = configparser.ConfigParser()
config.read("settings.SECRET.ini")

# ----------------------------------------------------------------------------

SYMBOL = 'BTC/EUR'

exchange = ccxt.coinbasepro({
    'apiKey': config["coinbase"]["apiKey"],
    'password': config["coinbase"]["password"],
    'secret': config["coinbase"]["secret"],
    'verbose': False,  # False -> no HTTP log
    'enableRateLimit': True
})

heiken_ashi_candles = []

# ----------------------------------------------------------------------------


def get_exchange_price(symbol):
    exchange = ccxt.coinbasepro({
        'apiKey': config["coinbase"]["apiKey"],
        'password': config["coinbase"]["password"],
        'secret': config["coinbase"]["secret"],
        'verbose': False,  # False -> no HTTP log
        'enableRateLimit': True
    })
    ticker = exchange.fetch_ticker(symbol)
    return json.dumps(ticker["info"]["price"])


def get_new_open(previous_close):
    current_open = previous_close
    while previous_close == current_open:
        time.sleep(13)
        current_open = get_exchange_price(SYMBOL)
    print("Last price: {} || Current Price: {}".format(previous_close, current_open))
    return current_open


def create_heiken_ashi_candle(timeframe, symbol):
    global heiken_ashi_candles
    current_time = datetime.datetime.now() - datetime.timedelta(hours=2, minutes=15)
    from_datetime = current_time.strftime('%Y-%m-%d %H:%M:%S')
    from_timestamp = exchange.parse8601(from_datetime)
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe, from_timestamp)
    high = ohlcv[0][2]
    low = ohlcv[0][3]
    custom_close = 0.25 * (ohlcv[0][1] + ohlcv[0][4] + ohlcv[0][3] + ohlcv[0][4])
    if len(heiken_ashi_candles) < 1:
        custom_open = 0.5 * (ohlcv[0][1] + ohlcv[0][3])
    else:
        previous_candle = heiken_ashi_candles[-1]
        custom_open = 0.5 * (heiken_ashi(previous_candle).open + heiken_ashi(previous_candle).close)
    custom_candle = heiken_ashi(high, custom_open, custom_close, low)
    heiken_ashi_candles.append(custom_candle)
    return custom_candle
