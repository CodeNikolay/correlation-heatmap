import yfinance as yf
import pandas as pd
import numpy as np

def get_tickers(tickers, start, end):
    prices_df = yf.download(tickers, start, end)['Close']
    return prices_df

def prices_to_returns(prices_df):
    return np.log(prices_df.pct_change().add(1)).dropna()