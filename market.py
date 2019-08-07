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

def monitor_prices():
    if datetime.utcnow().minute % 15 != 0:
        get_exchange_price()
