import websocket
import json
import numpy as np

class Exchange():
    def __init__(self, stream, tickers):
        self.wsapp = websocket.WebSocketApp(stream, on_message=self.on_message, on_open=self.on_open, on_close=self.on_close)
        self.tickers = tickers

        self.delta = 0
        self.buy = 0
        self.sell = 0

        self.market_buys = 0
        self.market_sells = 0

        self.bid_sizes = []
        self.ask_sizes = []


    def on_open(self, message):
        self.wsapp.send(json.dumps({
            "method": "SUBSCRIBE",
            "params": self.tickers,
            "id": 1
        }))

    def on_close(self):
        print('Exchange: UNSUBSCRIBED')
        self.wsapp.send(json.dumps({
            "method": "UNSUBSCRIBE",
            "params": self.tickers,
            "id": 312
        }))


    def on_message(self, wsapp, message):
        message = json.loads(message)
        self.set_delta(message['data'])
        # print(str(self.delta[0]) + " | Delta: " + str(self.delta[1]))


    def set_delta(self, data):
        print(data)
        pass
        # if data['m'] == False:
        #     self.buy = self.buy + np.multiply(float(data['p']), float(data['q']))
        #     self.market_buys += 1
        #     self.bid_sizes.append(float(self.buy).__round__(2))
        # elif data['m'] == True:
        #     self.sell = self.sell + np.multiply(float(data['p']), float(data['q']))
        #     self.market_sells += 1
        #     self.ask_sizes.append(float(self.sell).__round__(2))
        
        # self.delta = [data['s'], float(self.buy - self.sell).__round__(2)]
        # print(self.delta)



base_url = 'wss://stream.binance.com:9443/ws'
tickers = [
    "btcusdt@aggTrade",
    "ethusdt@aggTrade",
    "bnbusdt@aggTrade",
]
binance = Exchange(base_url, tickers)
binance.wsapp.run_forever()