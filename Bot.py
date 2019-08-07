# -----------------------------------------------------------------------------
import asyncio
import configparser
import json
import os
import sys
import time
from datetime import datetime
from twisted.internet import task, reactor
from pprint import pprint

import ccxt

import market
# -----------------------------------------------------------------------------
from heiken_ashi import heiken_ashi

this_folder = os.path.dirname(os.path.abspath(__file__))
root_folder = os.path.dirname(os.path.dirname(this_folder))
sys.path.append(root_folder + '/python')
sys.path.append(this_folder)

# -----------------------------------------------------------------------------

TIMEOUT = 60.0
REQUIRED_CANDLES = 2
SYMBOL = "BTC/EUR"
TIMEFRAME = "3m"

# -----------------------------------------------------------------------------

long = True

# -----------------------------------------------------------------------------


def wait_full_minute():
    t = datetime.utcnow()
    sleeptime = 60 - (t.second + t.microsecond / 1000000.0)
    print("waiting for {} seconds until {}...".format(sleeptime, datetime.utcnow().minute + 1))
    time.sleep(sleeptime)


def long_or_short():
    global long
    candles = market.heiken_ashi_candles
    previous_candle = candles[-2]
    current_candle = candles[-1]
    if len(candles > REQUIRED_CANDLES):
        if heiken_ashi(current_candle).close > heiken_ashi(current_candle).open > heiken_ashi(previous_candle).close:
            print("{} || GOING LONG @ {}".format(datetime.now(), market.get_exchange_price(SYMBOL)))
        elif heiken_ashi(current_candle).close < heiken_ashi(current_candle).open < heiken_ashi(previous_candle).close:
            print("{} || GOING LONG @ {} ".format(datetime.now(), market.get_exchange_price(SYMBOL)))
        else:
            print("{} || IDLE".format(datetime.now()))


market.create_heiken_ashi_candle(TIMEFRAME, SYMBOL)
while True:
     if datetime.utcnow().minute % 15 != 0:
         continue
     market.create_heiken_ashi_candle(TIMEFRAME, SYMBOL)
     long_or_short()
     wait_full_minute()
