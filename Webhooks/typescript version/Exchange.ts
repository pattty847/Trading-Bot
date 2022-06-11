class Exchange {
    SPOT_ENDPOINT = 'wss://stream.binance.com:9443'
    FUTURES_ENDPOINT = 'wss://fstream.binance.com'
    COMBINED_STREAMS = '/stream?streams='
    SINGLE_STREAM = '/ws/'
    GGTRADE = '@aggTrade'
    TRADE = '@trade'
    KLINE = '@kline_'
    MINI = '@miniTicker'

    STREAM: string
    STREAM_T: string
    WEBSOCKET: WebSocket
    ONOPEN: any
    ONMESSAGE: any
    ONERROR: any
    ONCLOSE: any

    constructor(exchange: string, single: boolean, market: string, ticker: string, stream: string) {
        this.STREAM = market + single ? this.SINGLE_STREAM : this.COMBINED_STREAMS + ticker + stream
        this.WEBSOCKET = new WebSocket(this.STREAM);
        this.ONOPEN = this.WEBSOCKET.onopen
        this.ONMESSAGE = this.WEBSOCKET.onmessage
        this.ONERROR = this.WEBSOCKET.onerror
        this.ONCLOSE = this.WEBSOCKET.onclose
    }
}


interface Exchange {
    ENDPOINT: string, 
    SINGLE: boolean, 
    STREAM: string,
}