from genericpath import isdir, isfile
from ccxt.base.decimal_to_precision import ROUND_UP
from configparser import ConfigParser
import ccxt.async_support as ccas
import ccxt
import pandas as pd
import time
import os


class Exchange:

    config_file = ConfigParser()
    config_file.read('C:\\Users\\pattt\\Desktop\\exchanges.config')


    def __init__(self, exchange_):
        self.exchange = exchange_
        self.config = self.config_file
        self.tickers = None
        self.bars = None
        self.api = None
        self.running = False
        self.connectExchange()


    def saveHistory(self, timeframe):
        file = 'ohlc/' + self.pair.replace('/', '-') + '-' + timeframe + '.csv'
        self.bars.to_csv(file, mode='a', index=False, header=False)


    # This will be the function that retrieves the next bar
    def fetchNextBar(self, timeframe, pair):
        self.running = True
        interval = self.api.parse_timeframe(timeframe)
        while(self.running):
            new_ohlcv = pd.DataFrame(self.api.fetch_ohlcv(pair, timeframe, limit=1))
            self.bars.append(new_ohlcv)
            print(self.bars)
            time.sleep(interval)

    # This function checks if we have a file with ohlc history for said coin and updates the timeframes we have missed since last run
    def loadHistory(self, timeframe, pair_, limit_):
        # Stores the actual name of the CSV file containing OHLCV data
        # Format: 'BTC-USD-5m.csv'
        ohlcv_file = pair_.replace('/', '-') + '-' + timeframe + '.csv'
        ohlcv_path = 'OHLCV/' + self.exchange + "/" + ohlcv_file
        print(self.tickers)
        if(pair_ in self.tickers):
            # Check if the file already exists and if so just load it and update the new OHLCV data
            if(isfile(ohlcv_path)):
                # Read in the file
                self.bars = pd.read_csv(ohlcv_path)
                # grab the last time since updated: last row in the time column
                last_update_time = self.bars.iloc[-1, 0]
                # pull the new OHLCV data since the last_update_time
                new_data = pd.DataFrame(self.api.fetch_ohlcv(pair_, timeframe, limit=limit_, since=last_update_time))
                # drop the first row which is the same as the last row we have in the CSV file
                new_data.drop(new_data.head(1).index, inplace=True)
                # append (update) the new data to the CSV file
                new_data.to_csv(ohlcv_path, mode='a', index=False, header=False)
                # reload the bars from the CSV file
                self.bars = pd.read_csv(ohlcv_path)
            else:
                # if it doesn't exist check if the 'OHLCV' folder exists
                if not isdir('OHLCV/' + self.exchange + '/'):
                    # if not make it pls
                    os.makedirs('OHLCV/' + self.exchange + '/')
                    # store the OHLCV data
                    self.bars = pd.DataFrame(self.api.fetch_ohlcv(pair_, timeframe, limit=limit_))
                    self.bars.to_csv(ohlcv_path, index=False)
                else:
                    # if we do have the 'OHLCV/exchange/coin.csv' file grab that shit
                    if not (isfile('OHLCV/' + self.exchange + '/' + ohlcv_file)):
                        self.bars = pd.DataFrame(self.api.fetch_ohlcv(pair_, timeframe, limit=limit_))
                        self.bars.to_csv(ohlcv_path, index=False)
        else:
            print(pair_ + ' does not exist on ' + self.exchange)


    # This is called first to make a connection to the exchange from the CONFIG file
    def connectExchange(self):
        exchange_class = getattr(ccxt, self.exchange)
        if(self.exchange.upper() in self.config):
            try:
                self.api = exchange_class({
                    'apiKey': self.config[self.exchange.upper()]['apiKey'],
                    'secret': self.config[self.exchange.upper()]['secret'],
                })
                self.tickers = self.api.tickers
                print(self.exchange + " - Connected and Tradable")
            except ccxt.NetworkError as e:
                print(e)
            except ccxt.ExchangeError as e:
                print(e)
            except Exception as e:
                print(e)
        else: 
            self.api = exchange_class()
            self.tickers = self.api.tickers
            print(self.exchange + " - Connected but NOT Tradable")
