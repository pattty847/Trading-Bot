import ccxt.async_support as ccxta
import pandas as pd
import pandas_ta as ta
import time
import asyncio
from discord_webhook import DiscordWebhook
from asyncio import get_event_loop, gather
from ccxt.base.decimal_to_precision import ROUND_UP  # noqa: E402
from pprint import pprint

webhook = DiscordWebhook(url='https://discord.com/api/webhooks/935995833638346753/h0t2NYoxCRzRMor8_YGK9PpDuyZndXjyRLkf9vM5D8NpPz7gx7NOeSFHdfXXQIHUFsJY')

# This function will calculate the WaveTrend and push it to the object's wavetrend
def calculateWaveTrend(src, symbol, timeframe):
    chlen = 9
    avg = 12
    malen = 3
    oslevel = -53
    oblevel = 53


    tfSrc = src.copy(deep=True)

    tfSrc['HLC3'] = (tfSrc.iloc[:, 2] + tfSrc.iloc[:, 3] + tfSrc.iloc[:, 4]) / 3

    # ESA = Exponential Moving Average
    tfSrc['ESA'] = tfSrc['HLC3'].ewm(span=chlen, adjust=False).mean()

    # de = ema(abs(tfsrc - esa), chlen)
    tfSrc['DE'] = abs(tfSrc['HLC3'] - tfSrc['ESA']).ewm(span=chlen, adjust=False).mean()

    # ci = (tfsrc - esa) / (0.015 * de)
    tfSrc['CI'] = (tfSrc['HLC3'] - tfSrc['ESA']) / (0.015 * tfSrc['DE'])
    # wt1 = security(syminfo.tickerid, tf, ema(ci, avg))
    tfSrc['wt1'] = tfSrc['CI'].ewm(span=avg, adjust=False).mean()
    # wt2 = security(syminfo.tickerid, tf, sma(wt1, malen))
    tfSrc['wt2'] = tfSrc['wt1'].rolling(malen).mean()
    tfSrc['wtVwap'] = tfSrc['wt1'] - tfSrc['wt2']
    tfSrc['wtOversold'] = tfSrc['wt2'] <= oslevel
    tfSrc['wtOverbought'] = tfSrc['wt2'] >= oblevel
    # see crossing(x, y) function
    tfSrc['wtCross'] = crossing(tfSrc['wt1'], tfSrc['wt2'])
    # determines if the cross above is bullish by being <= 0
    tfSrc['wtCrossUp'] = tfSrc['wt2'] - tfSrc['wt1'] <= 0
    # determines if the cross above is bearish by being <= 0
    tfSrc['wtCrossDown'] = tfSrc['wt2'] - tfSrc['wt1'] >= 0
    # see crossing(x, y) function (passing the series shifted to determine if the last row was a cross)
    tfSrc['wtCrosslast'] = crossing(tfSrc['wt1'].shift(-1), tfSrc['wt2'].shift(-1))
    tfSrc['wtCrossUplast'] = tfSrc['wt2'].shift(-1) - tfSrc['wt1'].shift(-1) <= 0
    tfSrc['wtCrossDownlast'] = tfSrc['wt2'].shift(-1) - tfSrc['wt1'].shift(-1) >= 0
    tfSrc['Symbol'] = symbol
    tfSrc['Timeframe'] = timeframe
    # Buy signal.
    tfSrc['Buy'] = tfSrc['wtCross'] & tfSrc['wtCrossUp'] & tfSrc['wtOversold']
    # Sell signal
    tfSrc['Sell'] = tfSrc['wtCross'] & tfSrc['wtCrossDown'] & tfSrc['wtOverbought']

    tfSrc.drop(tfSrc.head(50).index, inplace=True)
    # return the waveTrend DataFrame or return the last minute
    return (tfSrc)

"""
Lelec(bars, len) =>
    bindex = int(na)
    bindex := nz(bindex[1], 0)
    sindex = int(na)
    sindex := nz(sindex[1], 0)
    return = 0
    bindex := close > close[4] ? bindex + 1 : bindex
    sindex := close < close[4] ? sindex + 1 : sindex
    if bindex > bars and close < open and high >= highest(high, len)
        bindex := 0
        return := -1
        return
    else
        if sindex > bars and close > open and low <= lowest(low, len)
            sindex := 0
            return := 1
            return
"""


def exhuastion(src):
    tfSrc = src.copy(deep=True)
    length = 40
    bars = 10
    bindex = tfSrc.iloc[:, 2].shift(1)
    sindex = tfSrc.iloc[:, 2].shift(1)
    long = False
    # bindex = tfSrc.iloc[:, 2] > tfSrc.iloc[:, 2].shift(4) and 

    

# This function returns boolean values if x and y cross each other either up or down
def crossing(x, y):
    wtCross = []
    for i in range(len(x)):
        # check if the value wt1 is greater than wt2 AND less than the previous row OR the opposite for crossing down
        if(x.iloc[i] > y.iloc[i] and x.iloc[i-1] < y.iloc[i-1]) | (x.iloc[i] < y.iloc[i] and x.iloc[i-1] > y.iloc[i-1]):
            wtCross.append(True)
        else:
            wtCross.append(False)
    return wtCross


########################################################################################################################

async def fetch_ohlcv(exchange, symbol, timeframe, limit):
    since = None
    while True:
        try:
            ohlcv = await exchange.fetch_ohlcv(symbol, timeframe, since, limit)
            df = pd.DataFrame(ohlcv, columns=['Time', 'Open', 'High', 'Low', 'Close', 'Volume'])
            webhook.content = (calculateWaveTrend(df, symbol, timeframe).tail(1).iloc[0,-4:].to_string())
            webhook.execute()
            print('executed wh')
        except Exception as e:
            print(type(e).__name__, str(e))


async def async_client(exchange, symbol):
    client = getattr(ccxta, exchange)({'enableRateLimit': True})
    await client.load_markets()
    if symbol not in client.symbols:
        raise Exception(exchange + ' does not support symbol ' + symbol)
    while True:
        try:
            orderbook = await client.fetch_order_book(symbol)
            bids = orderbook['bids']
            asks = orderbook['asks']
            datetime = client.iso8601(client.milliseconds())
            # FORMAT - BIDS: [PRICE, QUANTITY], [PRICE, QUANTITY]
            # ORDERBOOK IMBALANCE - BIDS[0] - ASKS[0]
            imbalance = round(orderbook['bids'][0][1] - orderbook['asks'][0][1], 2)
            imbalance_percent = round((orderbook['bids'][0][1] - orderbook['asks'][0][1]) / (orderbook['bids'][0][1] + orderbook['asks'][0][1]), 2)
            
            # print(datetime, client.id, symbol, orderbook['bids'][0], orderbook['asks'][0], imbalance, imbalance_percent)
        except Exception as e:
            print(type(e).__name__, e.args, str(e))  # comment if not needed
            # break  # uncomment to break it
            # pass   # uncomment to do nothing and just retry again on next iteration
            # or add your own reaction according to the purpose of your app
    await client.close()


async def multi_orderbooks(exchanges, symbol):
    input_coroutines = [async_client(exchange, symbol) for exchange in exchanges]
    await asyncio.gather(*input_coroutines, return_exceptions=True)



async def main():
    exchange = ccxta.kucoin()
    exchange.enableRateLimit = True
    timeframe = '1d'
    limit = 200
    symbols = [ 'XPR/USDT']
    loops = [fetch_ohlcv(exchange, symbol, timeframe, limit) for symbol in symbols]
    await gather(*loops)
    await exchange.close()

# Consider review request rate limit in the methods you call
exchanges = ["kucoin"]
symbol = 'XPR/USDT'

asyncio.get_event_loop().run_until_complete(multi_orderbooks(exchanges, symbol))

# loop = get_event_loop()
# loop.run_until_complete(main())