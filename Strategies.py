import datetime

import market


class Stragety(object):

    def __init__(self):
        print("Created new Strategy")


class BarUpDnStrategy(Stragety):
    REQUIRED_CANDLES = 2
    SYMBOL = "BTC/EUR"

    def __init__(self):
        super().__init__()

    #USES HEIKIN ASHIN CANDLES! NOT DEFAULT
    #TODO dynamic candle desicion making
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


class MacDStrategy(Stragety):
    def __init__(self):
        super().__init__()

    def long_or_short(self):
        return False
