import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import streamlit as st
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from data_loader import *
from correlations import *

ASSET_DICT = {
    'S&P 500': 'SPY',
    'Nasdaq 100': 'QQQ',
    'Financials': 'XLF',
    'Energy': 'XLE',
    'Healthcare': 'XLV',
    'Industrials': 'XLI',
    'Utilities': 'XLU'
}

def assets_to_tickers(assets):
    return [ASSET_DICT[asset] for asset in assets]

col1, col2 = st.columns(2)
assets = col1.multiselect('Assets', list(ASSET_DICT.keys()), default=['S&P 500', 'Nasdaq 100'])
col11, col12 = col1.columns(2)
start_date = col11.date_input('Start','2026-01-01') # min and max values, dynamic default start?
end_date = col12.date_input('End') # min and max values, assert end > start, dynamic default end?

tickers = assets_to_tickers(assets)
returns_df = get_returns(tickers, start_date, end_date)
reindexed_prices_df = get_reindexed_prices(tickers, start_date, end_date)
full_corr = get_correlations(returns_df)
corr_selected = full_corr.loc[end_date - pd.DateOffset(1)]

fig = make_subplots(rows=2, cols=1, subplot_titles=['Price History', 'Correlation Heatmap'])
fig.add_trace(go.Scatter(x=reindexed_prices_df.index, y=reindexed_prices_df.values), row=2, col=1)
fig.add_heatmap(go.Figure(data=go.Heatmap(
    z = corr_selected.values,
    x = corr_selected.columns.tolist(),
    y = corr_selected.index.tolist(),
)), row=2, col=1)
col2.plotly_chart(fig, use_container_width=True, theme=None)