# -----------------------------------------------------------------------------
import os
import sys
import time
from datetime import datetime

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
TIMEFRAME = "1m"

# -----------------------------------------------------------------------------

long = False


# -----------------------------------------------------------------------------


def wait_full_minute():
    t = datetime.utcnow()
    sleeptime = 60 - (t.second + t.microsecond / 1000000.0)
    print("waiting for {} seconds until {}...".format(sleeptime, datetime.utcnow().minute + 1))
    time.sleep(sleeptime)


def long_or_short():
    global long
    candles = market.heiken_ashi_candles
    if len(candles) > REQUIRED_CANDLES:
        previous_candle = candles[-2]
        current_candle = candles[-1]
        if current_candle.close > current_candle.open > previous_candle.close and long is False:
            print("{} || GOING LONG @ {}".format(datetime.now(), market.get_exchange_price(SYMBOL)))
        elif current_candle.close < current_candle.open < previous_candle.close and long is True:
            print("{} || GOING SHORT @ {} ".format(datetime.now(), market.get_exchange_price(SYMBOL)))
        else:
            print("{} || IDLE".format(datetime.now()))


while True:
    market.monitor_prices(3)
    long_or_short()
