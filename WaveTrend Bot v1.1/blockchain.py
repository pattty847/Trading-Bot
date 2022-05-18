# Simple python websocket client
# https://github.com/websocket-client/websocket-client
from websocket import create_connection
options = {}
options['origin'] = 'https://exchange.blockchain.com'
url = "wss://ws.blockchain.info/mercury-gateway/v1/ws"
ws = create_connection(url, **options)
msg = '{"token": "{API_SECRET}", "action": "subscribe", "channel": "auth"}'
ws.send(msg)
result =  ws.recv()
print(result)
# { "seqnum":0,
#   "event":"subscribed",
#   "channel":"auth",
#   "readOnly":false }
ws.close()