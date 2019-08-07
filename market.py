# -----------------------------------------------------------------------------

import configparser
import datetime
import json
import operator
import threading
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



def monitor_prices():
    prices = {}
    while datetime.datetime.utcnow().minute % 2 != 0:
            prices[datetime.datetime.now()] = get_exchange_price("BTC/EUR")
            time.sleep(5)
    if len(heiken_ashi_candles) > 1:
        previous_heiken_ashi = heiken_ashi_candles[-1]
        candle_open = ((previous_heiken_ashi.open + previous_heiken_ashi.close)/2)
    else:
        candle_open = prices[list(prices.keys())[0]].strip('\"')
    candle_close = prices[list(prices.keys())[-1]].strip('\"')
    sortedprices = sorted(list(prices.values()))
    candle_high = sortedprices[-1].strip('\"')
    candle_low = sortedprices[0].strip('\"')
    custom_close = (float(candle_open) + float(candle_high) + float(candle_low) + float(candle_close) / 4)
    current_candle = heiken_ashi(float(candle_high), float(candle_open), float(candle_low), float(custom_close))
    heiken_ashi_candles.append(current_candle)

