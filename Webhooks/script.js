const webSocket = new WebSocket('wss://stream.binance.com:9443/ws/btcusdt@aggTrade');
const refresh_int = 200

// This will store the websocket data each message we receive
var data = 0

// This is where we will store the delta once calculated
var delta = 0

webSocket.onopen = function(event) {
    console.log('WebSocket [OPEN]')
}


webSocket.onmessage = function(event) {
    //console.log(event.data);
    var message = JSON.parse(event.data)
    data = message
    setDelta()
    setOrderSize(data['p'] * data['q'])
}


webSocket.onclose = function(event) {
    if (event.wasClean) {
        console.log('WebSocket [CLOSED]')
    } else {
        console.log('WebSocket [DIED]')
    }
}


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

    var count = 0
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


function drawPriceChart() {
    var layout = {
        title: {
            text: 'Price',
            font: {
                family: 'Courier New, monospace',
                size: 24
            },
            xref: 'paper',
            x: 0.05,
        },
        xaxis: {
            title: {
                text: 'Time',
                font: {
                    family: 'Courier New, monospace',
                    size: 18,
                    color: '#7f7f7f'
                }
            },
        },
        yaxis: {
            title: {
                text: 'Price',
                font: {
                    family: 'Courier New, monospace',
                    size: 18,
                    color: '#7f7f7f'
                }
            }
        }
    };


    // Plotly.newPlot(html-element, data, [layout], [config])
    Plotly.react('anything', [{
        y: [getPrice()],
        x: [getTime()],
        type: 'line'
    }], layout);


    setInterval(function() {
        Plotly.extendTraces('anything', {
            y: [
                [getPrice()]
            ],
            x: [
                [getTime()]
            ]
        }, [0])
    }, refresh_int)
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


var order = {
    'tiny': 0,
    'small': 0,
    'normal': 0,
    'large': 0,
    'chad': 0
}


function setOrderSize(size) {
    if (size > 0 && size < 10000) {
        order['tiny']++;
    }
    if (size > 10000 && size < 50000) {
        order['small']++;
    }
    if (size > 50000 && size < 100000) {
        order['normal']++;
    }
    if (size > 100000 && size < 250000) {
        order['large']++;
    }
    if (size > 250000 && size < 1000000) {
        order['chad']++
    }
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


drawPriceChart()
drawChart('delta', getTime, getDelta, 'line', 200, 1, 'Cummulative Delta', 'Time', 'Price')