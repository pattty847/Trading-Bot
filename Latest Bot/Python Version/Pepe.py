import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go

class Pepe():
    def __init__(self) -> None:
        pass

    def plot_ohlcv_matplotlib(self, df, subset=1000):
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


    def plot_ohlcv_plotly(self, df):
        df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        df['Date'] = pd.to_datetime(df['Date'], unit='ms')
        fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'])])

        fig.update_layout(
            title='Bitcoin',
            yaxis_title='Price',
            xaxis_title='Date',
            shapes = [dict(
                x0='2022-09-01', x1='2022-09-01', y0=0, y1=1, xref='x', yref='paper',
                line_width=2)],
            annotations=[dict(
                x='2022-09-01', y=0.05, xref='x', yref='paper',
                showarrow=False, xanchor='left', text='Test bar')]
        )
        fig.show()

pepe = Pepe()

df = pd.read_csv('binance_1d_2020-01-01.csv')
pepe.plot_ohlcv_plotly(df)

# pepe.plot_ohlcv_matplotlib(df)