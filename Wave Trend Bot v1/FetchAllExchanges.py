from ast import ExceptHandler
from pprint import pprint
import ccxt  # noqa: E402
import asyncio

def pullAllExchanges():
    all_exchanges = []
    for exchange_id in ccxt.exchanges:
        try:
            exchange = getattr(ccxt, exchange_id)()
            all_exchanges.append(exchange)
            # do what you want with this exchange
            # pprint(dir(exchange))
        except Exception as e:
            print(e)
    return all_exchanges

def findCoinInExchanges(coin, exchanges):
    results = []
    for exchange in exchanges:
        if exchange.fetch_ticker(coin):
            results.append(exchange)
    return results

allexchanges = pullAllExchanges()
# print(findCoinInExchanges('BTC/USDT', allexchanges))
answer = (asyncio.get_event_loop().run_until_complete(ccxt.binance().fetch_ticker('ETH/BTC')))
print(answer)