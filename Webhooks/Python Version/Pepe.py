import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go

class Pepe():
    def __init__(self) -> None:
        pass

    def plot_ohlcv(self, csv=None, subset=1000):
        df = pd.read_csv('binance.csv')
        df = df.tail(subset)
        df.columns = ['Time', 'Open', 'High', 'Low', 'Close', 'Volume']
        df['Time'] = pd.to_datetime(df['Time'], unit='ms')
        #create figure
        plt.figure()

        #define width of candlestick elements
        width = .4
        width2 = .05

        up = df[df.Close >= df.Open]
        down = df[df.Close < df.Open]

        col1 = 'green'
        col2 = 'red'

        plt.bar(up.index, up.Close - up.Open, width, bottom=up.Open, color=col1)
        plt.bar(up.index, up.High - up.Close, width2, bottom=up.Close, color=col1)
        plt.bar(up.index, up.Low - up.Open, width2, bottom=up.Open, color=col1)

        plt.bar(down.index, down.Close - down.Open, width, bottom=down.Open, color=col2)
        plt.bar(down.index, down.High - down.Close, width2, bottom=down.Open, color=col2)
        plt.bar(down.index, down.Low - down.Open, width2, bottom=down.Close, color=col2)

        plt.show()


    def plot_ohlcv_plotly(self):
        df = pd.read_csv('binance_1d_2020-01-01.csv')
        df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        df['Date'] = pd.to_datetime(df['Date'], unit='ms')
        fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'])])
        fig.show()

pepe = Pepe()

pepe.plot_ohlcv_plotly()