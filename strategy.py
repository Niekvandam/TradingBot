# Imports
# -----------------------------------------------------------------------------
import datetime
import market
import indicator


# Universal variables used throughout the class
# -----------------------------------------------------------------------------
SYMBOL = "BTC/USDT"

# The base strategy class
# -----------------------------------------------------------------------------

class Strategy(object):

    def __init__(self):
        print("Created new Strategy")

# The BarUpDnStrategy class
# -----------------------------------------------------------------------------

class BarUpDnStrategy(Strategy):
    REQUIRED_CANDLES = 2

    def __init__(self):
        super().__init__()

    # USES HEIKIN ASHIN CANDLES! NOT DEFAULT
    # TODO dynamic candle desicion making
    # TODO refactor code
    # Analyses the current market and decides whether to go long or short based on the previous opens/closes
    def long_or_short(self, long):
        global REQUIRED_CANDLES
        global SYMBOL
        curdate = datetime.now()
        candles = market.heikin_ashi_candles
        if len(candles) > REQUIRED_CANDLES:
            previous_candle = candles[-2]
            current_candle = candles[-1]
            if current_candle.close > current_candle.open and previous_candle.close > previous_candle.open and long is False or None:
                print("{} || GOING LONG @ {}".format(curdate, market.get_exchange_price(SYMBOL)))
                long = True
            elif current_candle.close < current_candle.open < previous_candle.close and long is True or None:
                print("{} || GOING SHORT @ {} ".format(curdate, market.get_exchange_price(SYMBOL)))
                long = False
            elif current_candle.open < current_candle.close < previous_candle.close and long is True or None:
                print("{} || GOING SHORT @ {} ".format(curdate, market.get_exchange_price(SYMBOL)))
                long = False
            else:
                print("{} || IDLE".format(curdate))
                long = None
        return long


# The MacdMaStrategy class
# -----------------------------------------------------------------------------
class MacdMaStrategy(Strategy):
    def __init__(self):
        super().__init__()

    # Analyses the current market and decides whether to go long or short based on Macd and MA
    def long_or_short(self, timeframe):
        if not len(market.default_candles) >= 100:
            market.create_ohlcv_list(100, timeframe)
        print("MACD is: {}".format(indicator.calculate_macd(market.ohlcv_data)))