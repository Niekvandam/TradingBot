# All imports
# -----------------------------------------------------------------------------
import os
import sys
import time
from datetime import datetime
import strategy

# Define where the root of the project is
# -----------------------------------------------------------------------------
this_folder = os.path.dirname(os.path.abspath(__file__))
root_folder = os.path.dirname(os.path.dirname(this_folder))
sys.path.append(root_folder + '/python')
sys.path.append(this_folder)

# Set universal values for testing purposes
# -----------------------------------------------------------------------------

SYMBOL = "BTC/USDT" # Default currency
TIMEFRAME = "5m" # Standard timeframe

# Misc. Methods
# -----------------------------------------------------------------------------

#Retrieve the current time, subtract the amount of seconds we are away from a new minute, and wait that amount of time
def wait_full_minute():
    t = datetime.utcnow()
    sleeptime = 60 - (t.second + t.microsecond / 1000000.0)
    time.sleep(sleeptime)

# The code to run
# -----------------------------------------------------------------------------

strategy.MacdMaStrategy.long_or_short(strategy, 5)
