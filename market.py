# -----------------------------------------------------------------------------

import configparser
import datetime
import json
import time

import ccxt

# -----------------------------------------------------------------------------

config = configparser.ConfigParser()
config.read("settings.SECRET.ini")

# ----------------------------------------------------------------------------

symbol = 'BTC/EUR'
# TODO fill lists with corresponding data
marketopens = []
marketcloses = []

# ----------------------------------------------------------------------------


def get_exchange_ticker(symbol):
    exchange = ccxt.coinbasepro({
        'apiKey': config["coinbase"]["apiKey"],
        'password': config["coinbase"]["password"],
        'secret': config["coinbase"]["secret"],
        'verbose': False,  # False -> no HTTP log
        'enableRateLimit': True
    })
    ticker = exchange.fetch_ticker(symbol)
    return ticker

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



# TODO REPEATING CODE
def get_market_open(symbol):
    ticker = get_exchange_ticker("BTC/EUR")
    current_market_open = json.dumps(ticker["info"]["price"])
    # print("Market open {} || {}".format(current_market_open, datetime.datetime.now()))
    return current_market_open


def get_market_close(symbol):
    ticker = get_exchange_ticker("BTC/EUR")
    previous_close = json.dumps(ticker["info"]["price"])
    # print("Market close {} || {}".format(previous_close, datetime.datetime.now()))
    return previous_close


def get_new_open(previous_close):
    current_open = previous_close
    while previous_close == current_open:
        time.sleep(13)
        ticker = get_exchange_ticker("BTC/EUR")
        current_open = json.dumps(ticker["info"]["price"])
    # print("New market open {} || {} ".format(current_open, datetime.datetime.now()))
    print("Last price: {} || Current Price: {}".format(previous_close, current_open))
    return current_open
