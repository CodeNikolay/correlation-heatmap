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

st.set_page_config(layout="wide")
col1, col2 = st.columns([1, 2])
assets = col1.multiselect('Assets', list(ASSET_DICT.keys()), default=['S&P 500', 'Nasdaq 100'])
col11, col12 = col1.columns(2)
start_date = col11.date_input('Start','2026-01-01') # min and max values, dynamic default start?
end_date = col12.date_input('End') # min and max values, assert end > start, dynamic default end?

tickers = assets_to_tickers(assets)
returns_df = get_returns(tickers, start_date, end_date)
reindexed_prices_df = get_reindexed_prices(tickers, start_date, end_date)

# version 1
fig1 = go.Figure()
for ticker in reindexed_prices_df.columns:
    fig1.add_trace(go.Scatter(x=reindexed_prices_df.index, y=reindexed_prices_df[ticker], mode='lines', name=ticker))
fig1.update_layout(
    title=dict(text='Assets over time', y=0.98, x=0.02, xanchor='left'),
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.05,
        xanchor='left',
        x=0
    ),
    margin=dict(l=50, r=20, t=80, b=20),
)
col2.plotly_chart(fig1)

corr_window = col2.slider(
    'Correlation window',
    min_value=start_date,
    max_value=end_date,
    value=(start_date, end_date),
    format='DD/MM/YYYY'
)

window_start, window_end = corr_window
corr = returns_df.loc[window_start:window_end].corr()

fig2 = go.Figure(data=go.Heatmap(
    z = corr.values,
    x = corr.columns.tolist(),
    y = corr.index.tolist(),
    zmin=-1,
    zmax=1
))
fig2.update_layout(
    title='Correlation Heatmap',
    margin=dict(l=50, r=20, t=40, b=20),
)
col2.plotly_chart(fig2, use_container_width=True, theme=None)


# # version 2
# corr_window = col1.slider(
#     'Correlation window',
#     min_value=start_date,
#     max_value=end_date,
#     value=(start_date, end_date),
#     format='DD/MM/YYYY'
# )
#
# window_start, window_end = corr_window
# corr = returns_df.loc[window_start:window_end].corr()
#
# fig = make_subplots(
#     rows=2, cols=1,
#     specs=[[{"type": "scatter"}], [{"type": "heatmap"}]],
#     subplot_titles=("Assets over time", "Correlation Heatmap")
# )
#
# for ticker in reindexed_prices_df.columns:
#     fig.add_trace(
#         go.Scatter(x=reindexed_prices_df.index, y=reindexed_prices_df[ticker], mode='lines', name=ticker),
#         row=1, col=1
#     )
#
# fig.add_trace(
#     go.Heatmap(
#         z=corr.values,
#         x=corr.columns.tolist(),
#         y=corr.index.tolist(),
#         zmin=-1,
#         zmax=1,
#         colorbar=dict(
#                     y=0.189,
#                     len=0.406,
#                 )
#     ),
#     row=2, col=1
# )
#
# fig.update_layout(
#     height=800,
#     # paper_bgcolor='rgba(0,0,0,0)',
#     plot_bgcolor='rgba(0,0,0,0)',
#     )
# fig.update_xaxes(showgrid=False, row=1, col=1)
# fig.update_yaxes(gridcolor='rgba(211,211,211,0.3)', row=1, col=1)
# col2.plotly_chart(fig, use_container_width=True, theme=None)