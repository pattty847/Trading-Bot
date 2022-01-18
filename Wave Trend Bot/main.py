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
    exchanges = ['gateio', 'ftx', 'coinbasepro']
    coin = 'BTC'
    currency = 'USD'
    pairs = [coin + '/' + currency]
    timeframe = '5m'
    # 30% of account balance to be used / trade
    trade_ratio_to_balance = .3

    all_exchanges = []

    # TO DO: Remove WaveTrend object creation from exchange/pairs loop. Append exchange to all_exchanges list.
    # Loop through all_exchanges to plot
    if __name__ == "__main__":
        for exchange in exchanges:
            for pair in pairs:
                e = Exchange(exchange, config_file, pair)
                e.loadHistory(timeframe)
                all_exchanges.append(e)
                print(e.bars)
        # aggregatedExchanges = ExchangeAggregator(all_exchanges)
                #wt = WaveTrend()
                #wt.calculateWaveTrend(e.bars)

                #print(e.bars)

                # e.bars.iloc[:, 4].plot()
                # e.bars.iloc[:, 11].plot()
                # plt.show()

startBot()