import ccxt
import time
import matplotlib.pyplot as plt
from configparser import ConfigParser
from LoadExchanges import Exchange
from WaveTrend import WaveTrend
from ExchangeAggregator import ExchangeAggregator

config_file = ConfigParser()
config_file.read('C:\\Users\\pattt\\Desktop\\exchanges.config')


def startBot():
    exchanges = ['ftx']
    coin = 'BTC'
    currency = 'USD'
    pairs = [coin + '/' + currency]
    timeframe = '1m'
    # 30% of account balance to be used / trade
    trade_ratio_to_balance = .3

    all_exchanges = []
    if __name__ == "__main__":
        for exchange in exchanges:
            for pair in pairs:
                # Exchange object used to get OHLCV data and do analysis on
                e = Exchange(exchange, config_file, pair, timeframe)
                print(e.fetchNextBar(timeframe))

startBot()