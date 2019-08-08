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


def monitor_prices(timespan):
    prices = {}
    # Run for a minute outside of the normal while loop IF utcnow is a multiple of timespan
    # If not done, the latter while loop would immediately be skipped resulting in an error
    if datetime.datetime.utcnow().minute % timespan == 0:
        while datetime.datetime.utcnow().minute % timespan == 0:
            prices[datetime.datetime.now()] = get_exchange_price("BTC/EUR")
            time.sleep(1)
    while datetime.datetime.utcnow().minute % timespan != 0:
            prices[datetime.datetime.now()] = get_exchange_price("BTC/EUR")
            time.sleep(1)
    candle_close = float(prices[list(prices.keys())[-1]].strip('\"'))
    sortedprices = sorted(list(prices.values()))
    candle_high = float(sortedprices[-1].strip('\"'))
    candle_low = float(sortedprices[0].strip('\"'))
    if len(heiken_ashi_candles) > 1:
        previous_heiken_ashi = heiken_ashi_candles[-1]
        candle_open = ((previous_heiken_ashi.open + previous_heiken_ashi.close)/2)
    else:
        candle_open = (float(prices[list(prices.keys())[0]].strip('\"')) + candle_close) / 2
    custom_close = ((candle_open + candle_high + candle_low + candle_close) / 4)
    current_candle = heiken_ashi(candle_high, candle_open, candle_low, custom_close)
    heiken_ashi_candles.append(current_candle)
    print("created candle || OPEN: {} || HIGH: {} || LOW: {} || CLOSE: {} ".format(candle_open, candle_high, candle_low, custom_close))

