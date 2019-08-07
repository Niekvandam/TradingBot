import configparser
import datetime
from pprint import pprint

from twisted.internet import task, reactor
import ccxt

import market

config = configparser.ConfigParser()
config.read("settings.SECRET.ini")

# -*- coding: utf-8 -*-

import os
import sys
import time

# -----------------------------------------------------------------------------

root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(root + '/python')

# -----------------------------------------------------------------------------

import ccxt  # noqa: E402

# -----------------------------------------------------------------------------
# common constants

msec = 1000
minute = 60 * msec
hold = 30

# -----------------------------------------------------------------------------


exchange = ccxt.coinbasepro({
        'apiKey': config["coinbase"]["apiKey"],
        'password': config["coinbase"]["password"],
        'secret': config["coinbase"]["secret"],
        'verbose': False,  # False -> no HTTP log
        'enableRateLimit': True
    })

# -----------------------------------------------------------------------------
precise_datetime = datetime.datetime.now() - datetime.timedelta(hours=1)
from_datetime = precise_datetime.strftime('%Y-%m-%d %H:%M:%S')
from_timestamp = exchange.parse8601(from_datetime)

# -----------------------------------------------------------------------------

now = exchange.milliseconds()
SYMBOL = "BTC/EUR"

# -----------------------------------------------------------------------------

data = []

long = False


def wait_full_minute():
    t = datetime.datetime.utcnow()
    sleeptime = 60 - (t.second + t.microsecond / 1000000.0)
    print("waiting for {} seconds until {}...".format(sleeptime, datetime.datetime.utcnow().minute))
    time.sleep(sleeptime)


def get_candles():
    global from_timestamp
    global data
    try:

        print(exchange.milliseconds(), 'Fetching candles starting from', exchange.iso8601(from_timestamp))
        ohlcvs = exchange.fetch_ohlcv(SYMBOL, '5m', from_timestamp)
        print(exchange.milliseconds(), 'Fetched', len(ohlcvs), 'candles')
        if len(ohlcvs) > 0:
            first = ohlcvs[0][0]
            last = ohlcvs[-1][0]
            print('First candle epoch', first, exchange.iso8601(first))
            print('Last candle epoch', last, exchange.iso8601(last))
            from_timestamp = ohlcvs[-1][0] + minute * 5  # good
            data += ohlcvs

    except (ccxt.ExchangeError, ccxt.AuthenticationError, ccxt.ExchangeNotAvailable, ccxt.RequestTimeout) as error:

        print('Got an error', type(error).__name__, error.args, ', retrying in', hold, 'seconds...')
        time.sleep(hold)


def long_or_short():
    global data, long
    if data[-1][1] > data[-1][4] > data[-2][1] and long is False:
        print("GOING LONG! at price {} || {}".format(market.get_exchange_price(SYMBOL), datetime.now()))
        long = True
    elif data[-1][1] < data[-1][4] < data[-2][1] and long is True:
        print("GOING SHORT! at price {} || {}".format(market.get_exchange_price(SYMBOL), datetime.now()))
        long = False
    else:
        print("IDLE || {}".format(datetime.datetime.now()))


candle_loop = task.LoopingCall(get_candles)
loopdeferred = candle_loop.start(30)

longOrShort = task.LoopingCall(long_or_short)
marketloop = longOrShort.start(60 * 5)

reactor.run() /  60