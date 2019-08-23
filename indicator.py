

# TODO add 9 bar EMA to MACD
# Calculate the macd with the past two Moving averages from both 12 and 26 timeframes
def calculate_macd(data):
    ma12 =calculate_ma(data, 12)
    ma26 = calculate_ma(data, 26)
    return ma12 - ma26


# Calculates the MA on basis of the given array of OHLCV's 'data', and the target length of the MA
def calculate_ma(data, length_of_ma):
    # Set default values to 0
    sum_of_ohlcv = 0.0000
    loopcount = 0

    # For each value in the ohlcv data attribute, loop through
    for ohlcv in reversed(data):
        # Increment loopcount until target length is met
        loopcount += 1

        if loopcount > length_of_ma:
            break
        # Create high and low average and divide those by each other
        high_average = (float(ohlcv[1]) + float(ohlcv[2])) / 2.0
        low_average = (float(ohlcv[3]) + float(ohlcv[4])) / 2.0
        current_average = (high_average + low_average) / 2.0
        sum_of_ohlcv += current_average

    # Divides the sum of all average ohlcv's by the target length of the MA's
    average = sum_of_ohlcv / length_of_ma

    return average


# TODO finish this method!
# Calculates the EMA on basis of the given array of OHLCV's 'data', and the target length of the EMA
def calculate_ema(data, length_of_ema):
    multiplier = (2 / (length_of_ema + 1))
    loopcount = 0
    sum_of_closes = 0
    for ohlcv in reversed(data):
        loopcount += 1
        if loopcount > length_of_ema:
            break
        sum_of_closes += ohlcv[4]
    sum_of_closes = sum_of_closes / length_of_ema

