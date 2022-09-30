const FUTURES_BTCUSDT_BNBUSDT_AGGTRADE = 'wss://fstream.binance.com/stream?streams=bnbusdt@aggTrade/btcusdt@aggTrade'
const SPOT_ENDPOINT = 'wss://stream.binance.com:9443'
const FUTURES_ENDPOINT = 'wss://fstream.binance.com'
const COMBINED_STREAMS = '/stream?streams='
const SINGLE_STREAM = '/ws/'

// After createStream() is called, this is where the STREAM variables are stored for future use
let STREAM = ''
let STREAM_TYPE = ''
let STREAM_END = ''

// Streams
const AGGTRADE = '@aggTrade'
const TRADE = '@trade'
const KLINE = '@kline_'
const MINI = '@miniTicker'

const PAIR = 'btcusdt'

// Here we assign a new WebSocket to the returned variable from createStream(endpoint, single/multi stream, ticker, stream)
const SOCKET = new WebSocket(createStream(SPOT_ENDPOINT, true, PAIR, AGGTRADE));

// Rate at which the chart will add a new data point from the socket stream
const refresh_int = 50

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
    setDelta()
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

// EXAMPLE: drawChart('delta', getTime, getDelta, 'line', refresh_int, 1, 'Cummulative Delta', 'Time', 'Delta')
function drawChart(div, x, y, type, refresh_rate, chart_length, title, xaxis, yaxis) {
    var layout = {
        title: {
            text: title,
            font: {
                family: 'Courier New, monospace',
                size: 24
            },
            xref: 'paper',
            x: 0.05,
        },
        xaxis: {
            title: {
                text: xaxis,
                font: {
                    family: 'Courier New, monospace',
                    size: 18,
                    color: '#7f7f7f'
                }
            },
        },
        yaxis: {
            title: {
                text: yaxis,
                font: {
                    family: 'Courier New, monospace',
                    size: 18,
                    color: '#7f7f7f'
                }
            }
        }
    };


    Plotly.react(div, [{
        x: [x()],
        y: [y()],
        type: type
    }], layout);

    setInterval(function() {
        Plotly.extendTraces(div, {
            x: [
                [x()]
            ],
            y: [
                [y()]
            ]
        }, [0])
    }, refresh_rate)
}


function getPrice() {
    return data['p']
}


function getTime() {
    return new Date(data['T'])
}


function getDelta() {
    return delta
}

function getOrderSize() {
    return order
}


function getOrders() {
    let size = 0
    if (data['m'] == false) {
        size = data['q']
    } else {
        size = -data['q']
    }
    return size
}


var buy = 0
var sell = 0

function setDelta() {
    if (data['m'] == false) {
        buy = buy + (data['p'] * data['q'])
    } else {
        sell = sell + (data['p'] * data['q'])
    }
    delta = (buy - sell)
}


//=======================================

drawChart('price-chart', getTime, getPrice, 'line', refresh_int, 1, 'Price Chart', 'Time', 'Price')
drawChart('delta-chart', getTime, getDelta, 'line', refresh_int, 1, 'Cummulative Delta', 'Time', 'Delta')
drawChart('orders-chart', getTime, getOrders, 'bar', refresh_int, 1, 'Order History', 'Time', 'Size')