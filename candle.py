# The default class for the bot to use. This will be using default high,
# low, open and closes to use for indicators and strategies.
class DefaultCandle:
    def __init__(self, candlehigh, candleopen, candlelow, candleclose):
        self.high = candlehigh
        self.open = candleopen
        self.low = candlelow
        self.close = candleclose


# Alternative to the DefaultCandle class for indicatory purposes.
# At this point in time, there is no functionality for this
class HeikinAshi:
    def __init__(self, candlehigh, candleopen, candlelow, candleclose):
        self.high = candlehigh
        self.open = candleopen
        self.low = candlelow
        self.close = candleclose
