import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import streamlit as st
import plotly.graph_objs as go
from data_loader import *
from correlations import *

ASSET_DICT = {
    "S&P 500": "SPY",
    "Nasdaq 100": "QQQ",
    "Financials": "XLF",
    "Energy": "XLE",
    "Healthcare": "XLV",
    "Industrials": "XLI",
    "Utilities": "XLU"
}

start = '2025-01-01'
end = '2026-01-01'

def assets_to_tickers(assets):
    return [ASSET_DICT[asset] for asset in assets]

assets = st.multiselect('Assets', list(ASSET_DICT.keys()), default=['S&P 500', 'Nasdaq 100'])

tickers = assets_to_tickers(assets)
returns_df = get_returns(tickers, start, end)
corr = get_correlations(returns_df)

fig = go.Figure(data=go.Heatmap(
    z = corr.values,
    x = corr.columns.tolist(),
    y = corr.index.tolist(),
))
st.plotly_chart(fig, use_container_width=True, theme=None)

# returns = np.log(prices.pct_change().add(1)).dropna()
# corr = returns.corr()
#
# fig, ax = plt.subplots()
# im = ax.imshow(corr, cmap='viridis')
# ax.set_xticklabels(labels=corr.columns)
# ax.set_yticklabels(labels=corr.columns)
# plt.show()