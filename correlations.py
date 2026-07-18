import pandas as pd
import streamlit as st

@st.cache_data
def get_correlation(returns_df: pd.DataFrame, start, end):
    return returns_df.loc[start:end].corr()