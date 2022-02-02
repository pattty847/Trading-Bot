import backtrader as bt

class Strategy(bt.Strategy):
    def next(self):
        pass

cerebro = bt.cerebro()

cerebro.addstrategy(Strategy)

cerebro.run()