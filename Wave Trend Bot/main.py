import ccxt
import time
import matplotlib.pyplot as plt
from configparser import ConfigParser
from LoadExchanges import Exchange
from WaveTrend import WaveTrend

config_file = ConfigParser()
config_file.read('C:\\Users\\pattt\\Desktop\\exchanges.config')


def mainBotThread(seconds, exchange):
    while(True):
        try:

            time.sleep(seconds)
        except ccxt.NetworkError as e:
            print(exchange.id, 'fetch_order_book failed due to a network error:', str(e))
        except ccxt.ExchangeError as e:
            print(e)
        except Exception as e:
            print(e)


def startBot():
    exchanges = ['gateio', 'binance', 'ftx']
    coin = 'BTC'
    currency = 'USDT'
    pairs = [coin + '/' + currency]
    timeframe = '1m'
    # 30% of account balance to be used / trade
    trade_ratio_to_balance = .3

    all_exchanges = []

    if __name__ == "__main__":
        for exchange in exchanges:
            for pair in pairs:
                e = Exchange(exchange, config_file, pair)
                e.loadHistory(timeframe)

                wt = WaveTrend()
                wt.calculateWaveTrend(e.bars)

                print(e.bars)

                #e.bars.iloc[:, 4].plot()
                # e.bars.iloc[:, 11].plot()
                #plt.show()

startBot()