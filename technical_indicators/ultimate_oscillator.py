# Import dependencies
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import datetime as dt
yf.pdr_override()

# input
symbol = "AAPL"
start = dt.date.today() - dt.timedelta(days=365)
end = dt.date.today()

# Read data
df = yf.download(symbol, start, end)

df["Prior Close"] = df["Adj Close"].shift()
df["BP"] = df["Adj Close"] - df[["Low", "Prior Close"]].min(axis=1)
df["TR"] = df[["High", "Prior Close"]].max(axis=1) - df[["Low", "Prior Close"]].min(
    axis=1
)
df["Average7"] = df["BP"].rolling(7).sum() / df["TR"].rolling(7).sum()
df["Average14"] = df["BP"].rolling(14).sum() / df["TR"].rolling(14).sum()
df["Average28"] = df["BP"].rolling(28).sum() / df["TR"].rolling(28).sum()
df["UO"] = (
    100 * (4 * df["Average7"] + 2 * df["Average14"] + df["Average28"]) / (4 + 2 + 1)
)
df = df.drop(["Prior Close", "BP", "TR", "Average7", "Average14", "Average28"], axis=1)

fig = plt.figure(figsize=(14, 7))
ax1 = plt.subplot(2, 1, 1)
ax1.plot(df["Adj Close"])
ax1.set_title("Stock " + symbol + " Closing Price")
ax1.set_ylabel("Price")
ax1.legend(loc="best")

ax2 = plt.subplot(2, 1, 2)
ax2.plot(df["UO"], label="Ultimate Oscillator")
# ax2.axhline(y=70, color='red')
# ax2.axhline(y=50, color='black', linestyle='--')
# ax2.axhline(y=30, color='red')
ax2.grid()
ax2.legend(loc="best")
ax2.set_ylabel("Ultimate Oscillator")
ax2.set_xlabel("Date")
plt.show()

# ## Candlestick with Ultimate Oscillator
from matplotlib import dates as mdates

dfc = df.copy()
dfc["VolumePositive"] = dfc["Open"] < dfc["Adj Close"]
# dfc = dfc.dropna()
dfc = dfc.reset_index()
dfc["Date"] = mdates.date2num(dfc["Date"].tolist())

from mplfinance.original_flavor import candlestick_ohlc

fig = plt.figure(figsize=(14, 7))
ax1 = plt.subplot(2, 1, 1)
candlestick_ohlc(ax1, dfc.values, width=0.5, colorup="g", colordown="r", alpha=1.0)
ax1.xaxis_date()
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%d-%m-%Y"))
ax1.grid(True, which="both")
ax1.minorticks_on()
ax1v = ax1.twinx()
colors = dfc.VolumePositive.map({True: "g", False: "r"})
ax1v.bar(dfc.Date, dfc["Volume"], color=colors, alpha=0.4)
ax1v.axes.yaxis.set_ticklabels([])
ax1v.set_ylim(0, 3 * df.Volume.max())
ax1.set_title("Stock " + symbol + " Closing Price")
ax1.set_ylabel("Price")

ax2 = plt.subplot(2, 1, 2)
ax2.plot(df["UO"], label="Ultimate Oscillator")
# ax2.axhline(y=70, color='red')
# ax2.axhline(y=50, color='black', linestyle='--')
# ax2.axhline(y=30, color='red')
ax2.grid()
ax2.legend(loc="best")
ax2.set_ylabel("Ultimate Oscillator")
ax2.set_xlabel("Date")
plt.show()
