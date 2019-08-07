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

this_folder = os.path.dirname(os.path.abspath(__file__))
root_folder = os.path.dirname(os.path.dirname(this_folder))
sys.path.append(root_folder + '/python')
sys.path.append(this_folder)

# -----------------------------------------------------------------------------

TIMEOUT = 60.0
REQUIRED_CANDLES = 2
SYMBOL = "BTC/EUR"


# -----------------------------------------------------------------------------

market_opens = []
market_closes = []
long = True

# -----------------------------------------------------------------------------


def wait_full_minute():
    t = datetime.utcnow()
    sleeptime = 60 - (t.second + t.microsecond / 1000000.0)
    print("waiting for {} seconds until {}...".format(sleeptime, datetime.utcnow().minute + 1))
    time.sleep(sleeptime)


def long_or_short():
    global long
    market_closes.append(market.get_market_close(SYMBOL))
    market_opens.append(market.get_new_open(market_closes[-1]))
    if len(market_closes) > REQUIRED_CANDLES:
        if market_closes[-1] > market_opens[-2] > market_closes[-2] and long is False:
            print("GOING LONG! at price {} || {}".format(market_opens[-1], datetime.now()))
            long = True
        elif market_closes[-1] < market_opens[-2] < market_closes[-2] and long is True:
            print("GOING SHORT! at price {} || {}".format(market_opens[-1], datetime.now()))
            long = False
        else:
            print("IDLE || {}".format(datetime.now()))


while True:
    if datetime.utcnow().minute % 3 == 0:
        long_or_short()
        wait_full_minute()
