import pandas as pd
import matplotlib.pyplot as plt
from exchange import Exchange as api
from pprint import pprint
from datetime import datetime

plt.style.use('dark_background')
plt.style.use('ggplot')
exchange = api('coinbasepro')

previos_order = None
# while True:
#     # Pull trades from exchange
while True:
    TRADES = exchange.fetch_trades(symbol='BTC/USDT')
    ORDERS = []
    for trades in TRADES:
        full_order = {trades['id']:trades['info']['time'], 'Price':trades['info']['price'], 'Size':trades['info']['size'], 'Side':trades['info']['side']}
        ORDERS.append(full_order)

    for each in range(len(ORDERS)):
        print(ORDERS[each])
    print('=======================================================================================')
    # Store the Time, Price, and Amount of trade
    # last_order = {'Time':ORDERS[-1]['datetime'], 'Price':ORDERS[-1]['price'], 'Amount':ORDERS[-1]['amount']}
    # Strip the format of Time so we can tell if it came after the previous time. (the api gives some out of order trades)
    # time_datetime = datetime.strptime(last_order['Time'], "%Y-%m-%dT%H:%M:%S.%fZ")
            
    
    #last_order.plot(kind='scatter', x=last_order['Price'], y=last_order['Amount'])
# BTC_ORDER_BOOK = exchange.fetch_data(symbol='BTC/USDT')

# bids = BTC_ORDER_BOOK[0][0:100].dropna(axis=0)
# asks = BTC_ORDER_BOOK[1][0:100].dropna(axis=0)

# bids['Size'] = bids['Size'].cumsum()6479292
# asks['Size'] = asks['Size'].cumsum()

# bids.plot(kind='line', x='Bids', y='Size', color='green')
# asks.plot(kind='line', x='Asks', y='Size', color='red')
# plt.show()


# if __name__ == '__main__':
#     exchanges = {
#         'coinbasepro': ['BTC/USDT']
#     }
#     asyncio_loop = get_event_loop()
#     asyncio_loop.run_until_complete(exchange.main(asyncio_loop, exchanges))