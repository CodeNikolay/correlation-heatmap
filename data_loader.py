import yfinance as yf
import numpy as np
import streamlit as st

@st.cache_data
def get_prices(tickers, start, end):
    prices_df = yf.download(tickers, start, end)['Close']
    return prices_df

@st.cache_data
def prices_to_returns(prices_df):
    return np.log(prices_df.pct_change().add(1)).dropna()

@st.cache_data
def get_returns(tickers, start, end):
    prices_df = get_prices(tickers, start, end)
    returns_df = prices_to_returns(prices_df)
    return returns_df

@st.cache_data
def get_reindexed_prices(prices_df):
    # prices_df = get_prices(tickers, start, end)
    reindexed_prices = (prices_df / prices_df.iloc[0]) * 100
    return reindexed_prices