import yfinance as yf
import pandas as pd
import numpy as np

def get_prices(tickers, start, end):
    prices_df = yf.download(tickers, start, end)['Close']
    return prices_df

def prices_to_returns(prices_df):
    return np.log(prices_df.pct_change().add(1)).dropna()

def get_returns(tickers, start, end):
    prices_df = get_prices(tickers, start, end)
    returns_df = prices_to_returns(prices_df)
    return returns_df