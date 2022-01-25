from genericpath import isfile, isdir
from configparser import ConfigParser
from discord_webhook import DiscordWebhook
from html2image import Html2Image
import WaveTrend as wt
import ccxt
import pandas as pd
import os
import time


class Exchange:

    config = ConfigParser()
    config.read('C:\\Users\\pattt\\Desktop\\Configs\\exchanges.config')
    webhook = 'https://discord.com/api/webhooks/935352230226321428/qAq064hZTM10FL90ITcLViTJjtpccfAeLDAwX6DXhuBaueyC50wGDi8yQgCpIFAYo_IJ'
    tradeview = 'https://www.tradingview.com/chart/KYErt3LL/'
    hti = Html2Image()
    

    def dispatchWebhook(self, src):
        wh = DiscordWebhook(url=self.webhook, content=src)
        response = wh.execute()
        print(response)


    def fetchLatestBar(self, ticker, timeframe):
        if(self.api.fetch_tickers(ticker)):
            interval = self.api.parse_timeframe(timeframe)
            while(True):
                time.sleep(interval)
                new_ohlcv = pd.DataFrame(self.api.fetch_ohlcv(ticker, timeframe, limit=1), index=None, columns=['Time', 'Open', 'High', 'Low', 'Close', 'Vol'])
                df = pd.concat([self.bars, new_ohlcv], ignore_index=True)
                self.bars = df
                wave = wt.calculateWaveTrend(df)
                #self.hti.screenshot(self.tradeview, save_as=f'{self.api.id}-{timeframe}.png')
                if (wave.iat[0, -2]):
                    self.dispatchWebhook(f"Buy: {wave.Close.to_string(index=False)}")
                elif(wave.iat[0, -1]): 
                    self.dispatchWebhook(f"Sell: {wave.Close.to_string(index=False)}")
        else:
            print(self.api.id + ' does not have '+ ticker)

    def updateHistory(self, tickers, timeframe):
        """ 
            Load exchange CSV file from 'OHLCV/' or create one and pull data.
        """
        for ticker in tickers:
            if(self.api.fetch_tickers(ticker)):
                PATH = 'OHLCV/' + self.api.id + '/'
                FILE = "{0}-{1}{2}".format(ticker.replace('/', '-'), timeframe, '.csv')
                if not isfile(PATH + FILE):
                    df = pd.DataFrame(self.api.fetch_ohlcv(ticker, timeframe), columns=['Time', 'Open', 'High', 'Low', 'Close', 'Vol'])
                    if not (isdir(PATH)):
                        os.makedirs(PATH)
                        df.to_csv(PATH + FILE, index=False)
                        self.bars = df
                    else: 
                        df.to_csv(PATH + FILE, index=False)
                        self.bars = df
                else:
                    self.bars = pd.read_csv(PATH + FILE)
                    last_update = self.bars.iloc[-1, 0]
                    new_data = pd.DataFrame(self.api.fetch_ohlcv(ticker, timeframe, since=int(last_update)))
                    new_data.drop(new_data.head(1).index, inplace=True)
                    new_data.to_csv(PATH + FILE, mode='a', header=False, index=False)
                    self.bars = pd.read_csv(PATH + FILE)
            else: 
                print(self.api.exchange.id + ' does not have '+ ticker)


    def loadExchange(self, exchange):
        exchange_class = getattr(ccxt, exchange)
        if(exchange.upper() in self.config):
            try:
                self.api = exchange_class({
                    'apiKey': self.config[exchange.upper()]['apiKey'],
                    'secret': self.config[exchange.upper()]['secret'],
                    #'pass': self.config[exchange.upper()]['pass'],
                })
                self.api.load_markets()
                # do what you want with this exchange
                print(exchange + ' connected, tradable')
            except ccxt.NetworkError as e:
                print(e)
            except ccxt.ExchangeError as e:
                print(e)
            except Exception as e:
                print(e)
        else: 
            self.api = exchange_class({
                'enableRateLimit': True,
            })
            self.api.load_markets()
            print(exchange + ' connected')


def runProgram():
    exchanges = ['binance', 'coinbasepro', 'gateio']
    pairs = ['BTC/USDT']
    timeframe = '1m'
    rows = 100
    all_exchanges = []
    for exchange in exchanges:
        e = Exchange()
        e.loadExchange(exchange)
        e.updateHistory(pairs, timeframe)
        e.fetchLatestBar(pairs[0], timeframe)

if __name__ == '__main__':
    runProgram()