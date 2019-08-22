# -----------------------------------------------------------------------------

import configparser
import datetime
import json
import time
from typing import List, Any

import ccxt

# -----------------------------------------------------------------------------
from candle import HeikinAshi, DefaultCandle

config = configparser.ConfigParser()
config.read("settings.SECRET.ini")

# ----------------------------------------------------------------------------

SYMBOL = 'BTC/EUR'

exchange = ccxt.binance({
    'apiKey': config["binance"]["apiKey"],
    'secret': config["binance"]["secret"],
    'verbose': False,  # False -> no HTTP log
    'enableRateLimit': True
})

default_candles: List[DefaultCandle] = []
heikin_ashi_candles: List[HeikinAshi] = []
ohlcv_data: List[tuple] = []
prices = {}


# ----------------------------------------------------------------------------

# TODO initialise exchange outside of method
def get_exchange_price(symbol):
    ticker = exchange.fetch_ticker(symbol)
    return json.dumps(ticker["info"]["price"])


# TODO Neccesary?
def get_new_open(previous_close):
    current_open = previous_close
    while previous_close == current_open:
        time.sleep(13)
        current_open = get_exchange_price(SYMBOL)
    print("Last price: {} || Current Price: {}".format(previous_close, current_open))
    return current_open


# TODO create non heikin-ashin candes
def create_heikin_ashi_candle(timespan):
    monitor_prices(timespan, False)
    candle_close = float(prices[list(prices.keys())[-1]].strip('\"'))
    sortedprices = sorted(list(prices.values()))
    candle_high = float(sortedprices[-1].strip('\"'))
    candle_low = float(sortedprices[0].strip('\"'))
    if len(heikin_ashi_candles) > 1:
        previous_heiken_ashi = heikin_ashi_candles[-1]
        candle_open = ((previous_heiken_ashi.open + previous_heiken_ashi.close) / 2)
    else:
        candle_open = (float(prices[list(prices.keys())[0]].strip('\"')) + candle_close) / 2
    custom_close = ((candle_open + candle_high + candle_low + candle_close) / 4)
    current_candle = HeikinAshi(candle_high, candle_open, candle_low, custom_close)
    heikin_ashi_candles.append(current_candle)
    print("created Heikin ashin || OPEN: {} || HIGH: {} || LOW: {} || CLOSE: {} ".format(candle_open, candle_high,
                                                                                         candle_low, custom_close))


# TODO remove redundant/double code
def create_default_candle(timespan):
    global ohlcv_data
    monitor_prices(timespan, False)
    candle_close = float(prices[list(prices.keys())[-1]].strip('\"'))
    candle_open = float(prices[list(prices.keys())[0]].strip('\"'))
    sortedprices = sorted(list(prices.values()))
    candle_high = float(sortedprices[-1].strip('\"'))
    candle_low = float(sortedprices[0].strip('\"'))
    ohlcv_data.append(exchange.milliseconds(), candle_open, candle_high, candle_low, candle_close, 0)
    current_candle = DefaultCandle(candle_high, candle_open, candle_low, candle_close)
    default_candles.append(current_candle)
    print("created candle || OPEN: {} || HIGH: {} || LOW: {} || CLOSE: {} ".format(candle_open, candle_high,
                                                                                   candle_low, candle_close))


# 'Monitors' the price for the given timespan(minutes) and fills a dictionary as result
def monitor_prices(timespan, retry):
    hold = 30
    if not retry: prices.clear()
    try:
        # Run for a minute outside of the normal while loop IF utcnow is a multiple of timespan
        # If not done, the latter while loop would immediately be skipped resulting in an error
        if datetime.datetime.utcnow().minute % timespan == 0:
            while datetime.datetime.utcnow().minute % timespan == 0:
                prices[datetime.datetime.now()] = get_exchange_price("BTC/USDT")
                time.sleep(1)
        while datetime.datetime.utcnow().minute % timespan != 0:
            prices[datetime.datetime.now()] = get_exchange_price("BTC/USDT")
            time.sleep(1)
    # TODO what errors are thrown?
    except:
        monitor_prices(timespan, True)


def create_ohlcv_list(candle_amount, timespan):
    global ohlcv_data
    ohlcv_data.clear()
    hold = 30
    timeframe = str(timespan) + "m"
    try:
        first_candle = exchange.milliseconds() - timespan * candle_amount * 60 * 1000  # current time - amount of candles * timespan per candle * minute * milliseconds
        ohlcv_data = exchange.fetch_ohlcv('BTC/USDT', timeframe, first_candle)
    except(ccxt.ExchangeError, ccxt.AuthenticationError, ccxt.ExchangeNotAvailable, ccxt.RequestTimeout) as error:
        print('Got an error', type(error).__name__, error.args, ', retrying in', hold, 'seconds...')
        time.sleep(hold)
        create_ohlcv_list(candle_amount, timespan)
