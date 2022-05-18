import os
import sys
import Strategies as wt
import pandas as pd
from asyncio import get_event_loop, gather
from tkinter import *

# -----------------------------------------------------------------------------

import ccxt.async_support as ccxt  # noqa: E402

# -----------------------------------------------------------------------------


print('CCXT Version:', ccxt.__version__)


async def fetch_ohlcv(exchange, symbol, timeframe, limit):
    since = None
    while True:
        try:
            ohlcv = await exchange.fetch_ohlcv(symbol, timeframe, since, limit)
            df = pd.DataFrame(ohlcv)
            if len(ohlcv):
                first_candle = ohlcv[0]
                datetime = exchange.iso8601(first_candle[0])
                # print(datetime, exchange.id, symbol, first_candle[1:])
                waveTrend = wt.calculateWaveTrend(df)
                print(waveTrend)
        except Exception as e:
            print(type(e).__name__, str(e))


async def main():
    exchange = ccxt.kucoin()
    exchange.enableRateLimit
    timeframe = '1m'
    limit = 100
    symbols = ['BTC/USDT']
    loops = [fetch_ohlcv(exchange, symbol, timeframe, limit) for symbol in symbols]
    await gather(*loops)
    await exchange.close()


loop = get_event_loop()
loop.run_until_complete(main())