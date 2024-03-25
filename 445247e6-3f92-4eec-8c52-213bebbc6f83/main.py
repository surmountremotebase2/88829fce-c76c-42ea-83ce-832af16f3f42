from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import SMA
from surmount.logging import log

class TradingStrategy(Strategy):
    def __init__(self):
        self.ticker = "SPY"  # Example with SPY ETF, a diversified representation of the US stock market
        self.short_window = 20  # Short-term moving average (SMA) window
        self.long_window = 50  # Long-term moving average (SMA) window

    @property
    def assets(self):
        return [self.ticker]

    @property
    def interval(self):
        return "1day"

    def run(self, data):
        # Calculate short-term and long-term SMAs for the chosen ticker
        short_sma = SMA(self.ticker, data["ohlcv"], length=self.short_window)
        long_sma = SMA(self.ticker, data["ohlcv"], length=self.long_window)

        if len(long_sma) == 0 or len(short_sma) == 0:
            return TargetAllocation({})

        # Trading signals based on moving average crossovers
        if short_sma[-1] > long_sma[-1] and short_sma[-2] <= long_sma[-2]:
            log(f"Going long on {self.ticker}, short SMA crossed above long SMA.")
            allocation = 1.0  # 100% allocation to go long on the asset
        elif short_sma[-1] < long_sma[-1] and short_sma[-2] >= long_sma[-2]:
            log(f"Exiting position in {self.ticker}, short SMA crossed below long SMA.")
            allocation = 0  # Exit position
        else:
            return TargetAllocation({})  # No action

        return TargetAllocation({self.ticker: allocation})