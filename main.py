import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

tickers = ["SPY", "QQQ", "XLF", "XLE", "XLV", "XLI", "XLU"]

prices = yf.download(tickers, start='2021-01-01', end='2026-01-01')['Close']
returns = np.log(prices.pct_change().add(1)).dropna()
corr = returns.corr()

fig, ax = plt.subplots()
im = ax.imshow(corr, cmap='viridis')
ax.set_xticklabels(labels=corr.columns)
ax.set_yticklabels(labels=corr.columns)
plt.show()