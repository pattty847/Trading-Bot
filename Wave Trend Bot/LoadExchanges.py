from msilib.schema import File
import ccxt
import pandas as pd
import pprint
import os


class Exchange:
    def __init__(self, exchange_, config_, pair_):
        self.exchange = exchange_
        self.config = config_
        self.pair = pair_
        self.bars = None
        self.api = None
        self.connectExchange()


    def saveHistory(self, timeframe):
        file = 'ohlc/' + self.pair.replace('/', '-') + '-' + timeframe + '.csv'
        self.bars.to_csv(file, mode='a', index=False, header=False)


    # This will be the function that retrieves the previous row of OHLCV data and appends it to the objects bars.
    async def fetchNextBar(self, timeframe):
        lastTF = pd.DataFrame(self.api.fetch_ohlcv(self.pair, timeframe, limit=1))
        self.bars.append(lastTF)


    # This function checks if we have a file with ohlc history for said coin and updates the timeframes we have missed since last run
    def loadHistory(self, timeframe):
        try:
            # String example: BTC-USDT-1m.csv
            file = self.pair.replace('/', '-') + '-' + timeframe + '.csv'
            # String example: OHLCV/binance/
            # Directory for storing the bars of data from the exchange for a certain timeframe
            ohlc_dir = 'OHLCV' + '/' + self.exchange + '/'
            os.makedirs(ohlc_dir)

            # Assign the OHLCV data to self.bars
            self.bars = pd.DataFrame(self.api.fetch_ohlcv(self.pair, timeframe))
            # Print self.bars to the OHLCV directory
            self.bars.to_csv(ohlc_dir + file, index=False, header=True)
        except FileExistsError:
            print('Loading History for: ' + file)
            print('Exchange: ' + self.exchange)

            # If the directory containing OHLCV data exists then load it
            OHLC_history = pd.read_csv(ohlc_dir + file)
            # Grab the last time since we have updated the file by indexing the last row's timestamp
            last_update_time = OHLC_history.iloc[-1, 0]

            # Create a new DataFrame with the new OHLCV we missed with the since parameter
            new_OHLC = pd.DataFrame(self.api.fetch_ohlcv(self.pair, timeframe, since=last_update_time))
            # Drip the first row becuase it's the same as the last row in the .csv file
            new_OHLC.drop(new_OHLC.head(1).index, inplace=True)
            # This will append the new OHLCV data to the .csv file
            new_OHLC.to_csv(ohlc_dir + file, mode='a', index=False, header=False)
            # Read the data into a DataFrame
            self.bars = pd.read_csv(ohlc_dir + file)

            
            # Remove the first 50 bars so our calculations are
            # self.bars.drop(self.bars.head(50).index, inplace=True)


    # This is called first to make a connection to the exchange from the CONFIG file
    def connectExchange(self):
        exchange_class = getattr(ccxt, self.exchange)
        if(self.exchange.upper() in self.config):
            try:
                self.api = exchange_class({
                    'apiKey': self.config[self.exchange.upper()]['apiKey'],
                    'secret': self.config[self.exchange.upper()]['secret'],
                })
                print(self.exchange + " - Connected and Tradable")
            except ccxt.NetworkError as e:
                print(e)
            except ccxt.ExchangeError as e:
                print(e)
            except Exception as e:
                print(e)
        else: 
            self.api = exchange_class()
            print(self.exchange + " - Connected but NOT Tradable")