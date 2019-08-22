# TODO create MacD
def create_macd(data):
    return None

# TODO create MA
def create_ma(data, amount_of_candles):
    sum_of_ohlcv = 0.0000
    loopcount = 0
    for ohlcv in reversed(data):
        loopcount += 1
        if loopcount > amount_of_candles:
            break
        high_average = (float(ohlcv[1]) + float(ohlcv[2])) / 2.0
        low_average = (float(ohlcv[3]) + float(ohlcv[4])) / 2.0
        current_average = (high_average + low_average) / 2.0
        print("Loop {} at time {} with value {}".format(loopcount, ohlcv[0], current_average))
        sum_of_ohlcv += current_average
    average = sum_of_ohlcv / amount_of_candles
    return average






#time open high low close volume