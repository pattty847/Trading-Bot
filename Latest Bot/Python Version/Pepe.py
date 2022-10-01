import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

class Pepe():
    def __init__(self) -> None:
        pass

    def plot_ohlcv_matplotlib(self, df, orders):
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


    def plot_orders(self, orders):
        area = orders['price_mean'] * orders['size_sum'] * 0.02
        time = pd.to_datetime(orders['timestamp'], unit='ms')
        plt.scatter(time, orders['price_mean'] * orders['size_sum'], s=area, c='red', alpha=0.5)
        plt.plot(time, orders['price_mean'])
        plt.show()


    def plot_ohlcv_plotly(self, df, orders):
        df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        df['Date'] = pd.to_datetime(df['Date'], unit='ms')
        fig = go.Figure(
            data=[go.Candlestick(
                    x=df['Date'],
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close'])])

        date = pd.to_datetime(orders['timestamp'], unit='ms')

        size = orders['size'] * 0.5

        fig.add_trace(go.Scatter(x=date, y=orders['price'], mode="markers", marker = dict(
                # color = orders['color'],
                size=size
            )
        ))

        fig.show()


pepe = Pepe()

df = pd.read_csv('btcusdt-orders.csv')
candles = pd.read_csv('btcusdt-candles.csv')

grouped_multiple = df.groupby(['timestamp']).agg({'size': ['sum'], 'price': ['mean'], 'side':['first']})
grouped_multiple.columns = ['size', 'price', 'side']
orders = grouped_multiple.reset_index()

orders = orders.loc[orders['size'] > 20]

# pepe.plot_orders(grouped_multiple)
pepe.plot_ohlcv_plotly(candles, orders)
# pepe.plot_ohlcv_matplotlib(df, grouped_multiple)