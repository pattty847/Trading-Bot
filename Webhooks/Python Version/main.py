import websocket

def on_message(wsapp, message):
    print(message)

tickers = ['bnbusdt', 'ethusdt', 'btcusdt']
stream = 'wss://stream.binance.com:9443/stream?streams={0}/{1}/{2}@aggTrade'.format(*tickers)

wsapp = websocket.WebSocketApp(stream, on_message=on_message)
wsapp.run_forever()