import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

stock = yf.Ticker('MSFT')
data = stock.history(period="100d")
data.to_csv('yahoo.csv')

df = pd.read_csv('yahoo.csv')
candlestick = go.Candlestick(x=df['Date'], open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])
fig = go.Figure(data=[candlestick])
fig.show()


fig.write_image("yourfile.png") 