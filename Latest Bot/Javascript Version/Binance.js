// const FUTURES_BTCUSDT_BNBUSDT_AGGTRADE = 'wss://fstream.binance.com/stream?streams=bnbusdt@aggTrade/btcusdt@aggTrade'
const SPOT_ENDPOINT = 'wss://stream.binance.com:9443'
const FUTURES_ENDPOINT = 'wss://fstream.binance.com'
const COMBINED_STREAMS = '/stream?streams='
const SINGLE_STREAM = '/ws/'

// Streams
const AGGTRADE = '@aggTrade'
const TRADE = '@trade'
const KLINE = '@kline_'
const MINI = '@miniTicker'

const PAIR = 'btcusdt'

// After createStream() is called, this is where the STREAM variables are stored for future use
let STREAM = ''
let STREAM_TYPE = ''
let STREAM_END = ''

// Here we assign a new WebSocket to the returned variable from createStream(endpoint, single/multi stream, ticker, type of stream)
const SOCKET = new WebSocket(createStream(SPOT_ENDPOINT, true, PAIR, AGGTRADE));

// Rate at which the chart will add a new data point from the socket stream
const refresh_int = 10

// This will store the SOCKET data each message we receive
var data = 0

// This is where we will store the delta once calculated
var delta = 0

SOCKET.onopen = function(event) {
    console.log('SOCKET [OPEN]')
}


SOCKET.onmessage = function(event) {
    //console.log(event.data);
    var message = JSON.parse(event.data)

    // This determines the stream feed type (multiple streams verse single)
    if (STREAM_TYPE == 'SINGLE') {
        data = message
    } else {
        data = message['data']
    }

    // After message is recieved here is where we call on functions to do stuff to the data

    setDelta()
    setOrderSize(data['p'] * data['q'])
}


SOCKET.onclose = function(event) {
    if (event.wasClean) {
        console.log('SOCKET [CLOSED]')
    } else {
        console.log('SOCKET [DIED]')
    }
}


function createStream(endpoint, single, ticker, stream) {
    if (single) {
        STREAM = endpoint + SINGLE_STREAM + ticker + stream
        STREAM_TYPE = 'SINGLE'
    } else {
        STREAM = endpoint + COMBINED_STREAMS + ticker + stream
        STREAM_TYPE = 'MULTI'
    }

    // Assign the stream endpoint if we're using SPOT or FUTURES, due to differences in order sizes
    STREAM_END = endpoint == SPOT_ENDPOINT ? 'SPOT' : endpoint == FUTURES_ENDPOINT ? 'FUTURES' : ''
    console.log(STREAM_END)
    return STREAM
}