from Exchange import Exchange
from Strategies import WaveTrend

import time


# def loadExchanges(exchanges, pairs, timeframe, rows):
#     if len(exchanges) > 1:
#         for exchange in exchanges:
#             for pair in pairs:
#                 exchangeObj = LoadExchange(exchange)
#                 exchangeObj.loadHistory(timeframe, pair, rows)
#                 waveTrendObj = WaveTrend()
#                 exchangeObj.fetchNextBar(timeframe, pair)
                
#     else:
#         exchangeObj = LoadExchange(exchanges[0])
#         waveTrendObj = WaveTrend()
#         for pair in pairs:
#             exchangeObj.loadHistory(timeframe, pair, rows)
#             exchangeObj.fetchNextBar(timeframe, pair)
#             # print(waveTrendObj.calculateWaveTrend(exchangeObj.bars))