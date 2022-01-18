import ccxt
import pandas as pd

# 9, 12, 3, -53, 53, False
class WaveTrend:
    def __init__(self):
        self.wavetrend = None
        self.chlen = 9
        self.avg = 12
        self.malen = 3
        self.oslevel = -53
        self.oblevel = 53


    # This function will calculate the WaveTrend and return them
    def calculateWaveTrend(self, src):
        # Load the data from 'coin' by 'timeframe' (1000 lines 0-999)
        # limit will show x bars of history
        # tfSrc = pd.DataFrame(exchange.fetch_ohlcv(coin, timeframe, limit=50))

        tfSrc = pd.DataFrame(src)

        tfSrc['HLC3'] = (tfSrc.iloc[:, 2] + tfSrc.iloc[:, 3] + tfSrc.iloc[:, 4]) / 3

        # ESA = Exponential Moving Average
        tfSrc['ESA'] = tfSrc['HLC3'].ewm(span=self.chlen, adjust=False).mean()

        # de = ema(abs(tfsrc - esa), chlen)
        tfSrc['DE'] = abs(tfSrc['HLC3'] - tfSrc['ESA']).ewm(span=self.chlen, adjust=False).mean()

        # ci = (tfsrc - esa) / (0.015 * de)
        tfSrc['CI'] = (tfSrc['HLC3'] - tfSrc['ESA']) / (0.015 * tfSrc['DE'])
        # wt1 = security(syminfo.tickerid, tf, ema(ci, avg))
        tfSrc['wt1'] = tfSrc['CI'].ewm(span=self.avg, adjust=False).mean()
        # wt2 = security(syminfo.tickerid, tf, sma(wt1, malen))
        tfSrc['wt2'] = tfSrc['wt1'].rolling(self.malen).mean()
        tfSrc['wtVwap'] = tfSrc['wt1'] - tfSrc['wt2']
        tfSrc['wtOversold'] = tfSrc['wt2'] <= self.oslevel
        tfSrc['wtOverbought'] = tfSrc['wt2'] >= self.oblevel
        # see crossing(x, y) function
        tfSrc['wtCross'] = self.crossing(tfSrc['wt1'], tfSrc['wt2'])
        # determines if the cross above is bullish by being <= 0
        tfSrc['wtCrossUp'] = tfSrc['wt2'] - tfSrc['wt1'] <= 0
        # determines if the cross above is bearish by being <= 0
        tfSrc['wtCrossDown'] = tfSrc['wt2'] - tfSrc['wt1'] >= 0
        # see crossing(x, y) function (passing the series shifted to determine if the last row was a cross)
        tfSrc['wtCrosslast'] = self.crossing(tfSrc['wt1'].shift(-1), tfSrc['wt2'].shift(-1))
        tfSrc['wtCrossUplast'] = tfSrc['wt2'].shift(-1) - tfSrc['wt1'].shift(-1) <= 0
        tfSrc['wtCrossDownlast'] = tfSrc['wt2'].shift(-1) - tfSrc['wt1'].shift(-1) >= 0
        # Buy signal.
        tfSrc['Buy'] = tfSrc['wtCross'] & tfSrc['wtCrossUp'] & tfSrc['wtOversold']
        # Sell signal
        tfSrc['Sell'] = tfSrc['wtCross'] & tfSrc['wtCrossDown'] & tfSrc['wtOverbought']

        tfSrc.drop(tfSrc.head(50).index, inplace=True)
        # return the waveTrend DataFrame or return the last minute
        self.wavetrend = tfSrc
        


    def crossing(self, x, y):
        wtCross = []
        for i in range(len(x)):
            # check if the value wt1 is greater than wt2 AND less than the previous row OR the opposite for crossing down
            if(x.iloc[i] > y.iloc[i] and x.iloc[i-1] < y.iloc[i-1]) | (x.iloc[i] < y.iloc[i] and x.iloc[i-1] > y.iloc[i-1]):
                wtCross.append(True)
            else:
                wtCross.append(False)
        return wtCross