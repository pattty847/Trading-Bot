import ccxt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from asyncio import gather

class Exchange:
    def __init__(self, exchange):
        try:
            self.exchange = getattr(ccxt, exchange)()
            self.exchange
            {
                "rateLimit": 1000,
                "enableRateLimit": True,
                # 'verbose': True,
            }
        except(ccxt.BaseError) as error:
            print('Trouble connecting to ', exchange, '- Error: ', error)
        print(exchange, ' initialized.')


    def fetch_data(self, symbol):
        try:
            orderbook = self.exchange.fetch_order_book(symbol)
            pd.set_option('display.float_format', lambda x: '%.4f' % x)
            bids = pd.DataFrame(orderbook['bids'], columns=['Bids', 'Size'])
            asks = pd.DataFrame(orderbook['asks'], columns=['Asks', 'Size'])
            return (bids, asks)
        except (ccxt.ExchangeError, ccxt.AuthenticationError, ccxt.ExchangeNotAvailable, ccxt.RequestTimeout) as error:
            print('Error', type(error).__name__, error.args)


    def fetch_trades(self, symbol):
        try: 
            orders = self.exchange.fetch_trades(symbol)
            return orders
        except (ccxt.ExchangeError, ccxt.AuthenticationError, ccxt.ExchangeNotAvailable, ccxt.RequestTimeout) as error:
            print('Error', type(error).__name__, error.args)


    def reject_outliers(data, m = 2.):
        d = np.abs(data - np.median(data))
        mdev = np.median(d)
        s = d/mdev if mdev else 0.
        return data[s<m]


    # async def symbol_loop(self, exchange, symbol):
    #     print('Starting the', exchange.id, 'symbol loop with', symbol)
    #     while True:
    #         try:
    #             orderbook = await exchange.fetch_order_book(symbol)
    #             now = exchange.milliseconds()
    #             print(exchange.iso8601(now), exchange.id, symbol, orderbook['asks'][0], orderbook['bids'][0])
    #             # --------------------> DO YOUR LOGIC HERE <------------------

    #         except Exception as e:
    #             print(str(e))
    #             # raise e  # uncomment to break all loops in case of an error in any one of them
    #             break  # you can break just this one loop if it fails


    # async def exchange_loop(self, asyncio_loop, exchange_id, symbols):
    #     print('Starting the', exchange_id, 'exchange loop with', symbols)
    #     exchange = getattr(ccxt, exchange_id)({
    #         'enableRateLimit': True,
    #         'asyncio_loop': asyncio_loop,
    #     })
    #     loops = [self.symbol_loop(exchange, symbol) for symbol in symbols]
    #     await gather(*loops)
    #     await exchange.close()


    # async def main(self, asyncio_loop, exchanges):
    #     loops = [self.exchange_loop(asyncio_loop, exchange_id, symbols) for exchange_id, symbols in exchanges.items()]
    #     await gather(*loops)