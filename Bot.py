# -----------------------------------------------------------------------------
import os
import sys
import time
from datetime import datetime

import indicator
import market
# -----------------------------------------------------------------------------
import strategy

this_folder = os.path.dirname(os.path.abspath(__file__))
root_folder = os.path.dirname(os.path.dirname(this_folder))
sys.path.append(root_folder + '/python')
sys.path.append(this_folder)

# -----------------------------------------------------------------------------

TIMEOUT = 60.0
REQUIRED_CANDLES = 2
SYMBOL = "BTC/USDT"
TIMEFRAME = "1m"


# -----------------------------------------------------------------------------


def wait_full_minute():
    t = datetime.utcnow()
    sleeptime = 60 - (t.second + t.microsecond / 1000000.0)
    print("waiting for {} seconds until {}...".format(sleeptime, datetime.utcnow().minute + 1))
    time.sleep(sleeptime)


strategy.MacdMaStrategy.long_or_short(strategy, 5)
