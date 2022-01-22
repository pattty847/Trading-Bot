from LoadExchanges import Exchange as LoadExchange
from WaveTrend import WaveTrend


def calculate(data):
    pass


def loadExchanges(exchanges, pairs, timeframe, rows):
    if len(exchanges) > 1:
        for exchange in exchanges:
            for pair in pairs:
                exchangeObj = LoadExchange(exchange)
                exchangeObj.loadHistory(timeframe, pair, rows)
                waveTrendObj = WaveTrend()
                exchangeObj.fetchNextBar(timeframe, pair)
                
    else:
        exchangeObj = LoadExchange(exchanges[0])
        waveTrendObj = WaveTrend()
        for pair in pairs:
            exchangeObj.loadHistory(timeframe, pair, rows)
            exchangeObj.fetchNextBar(timeframe, pair)
            # print(waveTrendObj.calculateWaveTrend(exchangeObj.bars))


def runProgram():
    exchanges = ['gateio', 'binance', 'ftx', 'coinbasepro']
    pairs = ['BTC/USDT', 'ETH/USDT']
    timeframe = '1m'
    rows = 100

    loadExchanges(exchanges, pairs, timeframe, rows)


if __name__ == '__main__':
    runProgram()