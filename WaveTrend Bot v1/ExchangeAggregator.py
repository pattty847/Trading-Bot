from configparser import ConverterMapping
from mimetypes import init
import pandas as pd
import numpy as np

class ExchangeAggregator:
    def __init__(self, exchanges_):
        self.exchanges = exchanges_
        self.aggregate()
        self.bars = None


    def aggregate(self):
        exchange_ohlc = []
        exchange_volume = []
        for exchange in self.exchanges:
            exchange_ohlc.append(exchange.bars.iloc[:, 1:5])
            exchange_volume.append(exchange.bars.iloc[:, -1])
        # agg_ohlc = pd.DataFrame(np.mean(exchange_ohlc)).round(2)
        # cum_vol = pd.DataFrame(np.sum(exchange_volume)).round(2)
        # agg_ohlc.to_csv('agg.csv')