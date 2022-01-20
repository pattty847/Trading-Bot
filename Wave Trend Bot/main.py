import ccxt
import time
import asyncio
import matplotlib.pyplot as plt
from pprint import pprint
from configparser import ConfigParser
from LoadExchanges import Exchange
from WaveTrend import WaveTrend
from ExchangeAggregator import ExchangeAggregator

config_file = ConfigParser()
config_file.read('C:\\Users\\pattt\\Desktop\\exchanges.config')


def startBot():
    exchanges = ['ftx', 'gateio']
    exchanges_test = ['ftx']
    coin = 'BTC'
    currency = 'USDT'
    pairs = ['BTC/USD']
    timeframe = '1h'
    # 30% of account balance to be used / trade
    trade_ratio_to_balance = .3

    all_exchanges = []
    if __name__ == "__main__":
        for exchange in exchanges:
            for pair in pairs:
                # Exchange object used to get OHLCV data and do analysis on
                e = Exchange(exchange, config_file, pair, timeframe)
                
                print(e.bars)

startBot()