# Import dependencies
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import datetime as dt
yf.pdr_override()

# input
symbol = "AAPL"
start = dt.date.today() - dt.timedelta(days=180)
end = dt.date.today()

# Read data
df = yf.download(symbol, start, end)

df["Pivot"] = (df["High"] + df["Low"] + df["Adj Close"]) / 3.0
df["BC"] = (df["High"] + df["Low"]) / 2.0
df["TC"] = (df["Pivot"] - df["BC"]) + df["Pivot"]

plt.figure(figsize=(14, 7))
plt.plot(df["Adj Close"])
plt.plot(df["TC"], label="Central Pivot Range")
plt.plot(df["Pivot"], label="Central Pivot Range")
plt.plot(df["BC"], label="Central Pivot Range")
plt.title("Stock " + symbol + " Closing Price")
plt.ylabel("Price")
plt.legend(loc="best")
plt.show()

# ## Candlestick with Central Pivot Range (CPR)
from matplotlib import dates as mdates

dfc = df.copy()
dfc["VolumePositive"] = dfc["Open"] < dfc["Adj Close"]
# dfc = dfc.dropna()
dfc = dfc.reset_index()
dfc["Date"] = pd.to_datetime(dfc["Date"])
dfc["Date"] = dfc["Date"].apply(mdates.date2num)
from mplfinance.original_flavor import candlestick_ohlc

fig = plt.figure(figsize=(32, 25))
ax1 = plt.subplot(2, 1, 1)
ax1.plot(df["Pivot"], label="Pivot")
ax1.plot(df["BC"], label="BC")
ax1.plot(df["TC"], label="TC")
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
ax1.legend(loc="best")
plt.show()
