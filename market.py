# -----------------------------------------------------------------------------

import configparser
import datetime
import json
import time
from typing import List, Any
from candle import HeikinAshi, DefaultCandle
import ccxt

# Set up the configparser for further reading
# -----------------------------------------------------------------------------

config = configparser.ConfigParser()
config.read("settings.SECRET.ini")

# Set universal values for testing purposes
# -----------------------------------------------------------------------------

SYMBOL = 'BTC/USDT'

exchange = ccxt.binance({
    'apiKey': config["binance"]["apiKey"],
    'secret': config["binance"]["secret"],
    'verbose': False,  # False -> no HTTP log
    'enableRateLimit': True
})

#List with heikin ashi candles and list with ohlcv candles
heikin_ashi_candles: List[HeikinAshi] = []
ohlcv_data: List[tuple] = []
#Prices dict, used for the creation of heikin ashi
prices = {}

# Methods that need a reference to the exchange
# ----------------------------------------------------------------------------


# TODO initialise exchange outside of method
# Gets the current exchange price of the given symbol by requesting the ticker
def get_exchange_price(symbol):
    ticker = exchange.fetch_ticker(symbol)
    return json.dumps(ticker["info"]["price"])


# TODO create non heikin-ashin candes
# Monitors the price for the given timespan, and creates a heikin ashi from it afterwards
def create_heikin_ashi_candle(timespan):
    # Call the method to scan the price action for the given timespan
    monitor_prices(timespan, False)

    # Create the first 3 of the ohlc pair.
    candle_close = float(prices[list(prices.keys())[-1]].strip('\"'))
    sortedprices = sorted(list(prices.values()))
    candle_high = float(sortedprices[-1].strip('\"'))
    candle_low = float(sortedprices[0].strip('\"'))

    # If any heikin ashi candles already exist, calculate the open with the previous open/close
    if len(heikin_ashi_candles) > 1:
        previous_heiken_ashi = heikin_ashi_candles[-1]
        candle_open = ((previous_heiken_ashi.open + previous_heiken_ashi.close) / 2)

    # If this is the first heikin ashi, use the default open/close pricing
    else:
        candle_open = (float(prices[list(prices.keys())[0]].strip('\"')) + candle_close) / 2

    # Calculate the custom close that the heikin ashi brings with him.
    # Open, high, low, close / 4 = new close
    custom_close = ((candle_open + candle_high + candle_low + candle_close) / 4)

    #Create and append candle
    current_candle = HeikinAshi(candle_high, candle_open, candle_low, custom_close)
    heikin_ashi_candles.append(current_candle)
    print("created Heikin ashin || OPEN: {} || HIGH: {} || LOW: {} || CLOSE: {} ".format(candle_open, candle_high,
                                                                                         candle_low, custom_close))


# TODO remove redundant/double code
# TODO default candle is not saved
# Creates a default candle with the OHLC rhetoric
def create_default_candle(timespan):
    # Defines the global list OHLCV data to append to
    global ohlcv_data

    # Monitor the price action for the given timespan
    monitor_prices(timespan, False)

    # Create the open/high/low/close with the monitored price action
    candle_close = float(prices[list(prices.keys())[-1]].strip('\"'))
    candle_open = float(prices[list(prices.keys())[0]].strip('\"'))

    #Sort the prices to value (price of given pair) to get the high and low
    sortedprices = sorted(list(prices.values()))
    candle_high = float(sortedprices[-1].strip('\"'))
    candle_low = float(sortedprices[0].strip('\"'))

    #Add ohlcv data to the ohlcv data list
    ohlcv_data.append(exchange.milliseconds(), candle_open, candle_high, candle_low, candle_close, 0)
    current_candle = DefaultCandle(candle_high, candle_open, candle_low, candle_close)


# 'Monitors' the price for the given timespan(minutes) and fills a dictionary as result
def monitor_prices(timespan, retry):
    hold = 30
    if not retry: prices.clear()

    #Try and execute code, if code fails go to exception
    try:

        # Run for a minute outside of the normal while loop IF utcnow is a multiple of timespan
        # If not done, the latter while loop would immediately be skipped resulting in an error
        if datetime.datetime.utcnow().minute % timespan == 0:

            # Run until the time in minutes is a multiple of the timespan
            while datetime.datetime.utcnow().minute % timespan == 0:
                prices[datetime.datetime.now()] = get_exchange_price("BTC/USDT")
                time.sleep(1)

        #Run until the time in minutes is a multiple of the timespan
        while datetime.datetime.utcnow().minute % timespan != 0:
            prices[datetime.datetime.now()] = get_exchange_price("BTC/USDT")
            time.sleep(1)

    # TODO what errors are thrown?
    # Catches errors
    except:
        monitor_prices(timespan, True)


# Creates a list with the ohlcvs from the last 'timespan'
def create_ohlcv_list(candle_amount, timespan):
    # Define the global ohlcv data list, to append to
    global ohlcv_data

    # Clear out the ohlcv list, to start fresh
    ohlcv_data.clear()
    hold = 30

    # Append 'm' to the timespan, to retrieve the ohlvc data of timespan'm'
    timeframe = str(timespan) + "m"

    # Try and execute code, if code fails go to exception
    try:
        first_candle = exchange.milliseconds() - timespan * candle_amount * 60 * 1000  # current time - amount of candles * timespan per candle * minute * milliseconds
        ohlcv_data = exchange.fetch_ohlcv('BTC/USDT', timeframe, first_candle)

    # TODO check error references?
    # Catch errors
    except(ccxt.ExchangeError, ccxt.AuthenticationError, ccxt.ExchangeNotAvailable, ccxt.RequestTimeout) as error:
        print('Got an error', type(error).__name__, error.args, ', retrying in', hold, 'seconds...')
        time.sleep(hold)
        create_ohlcv_list(candle_amount, timespan)
