import pandas as pd
import numpy as np

def get_correlations(returns_df: pd.DataFrame, window=21, step=1):
    corr_df = returns_df.rolling(window=window).corr()
    return corr_df

