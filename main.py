from datetime import timedelta

import plotly.graph_objs as go

from data_loader import *
from correlations import get_correlation

ASSET_DICT = {
    'S&P 500': 'SPY',
    'Nasdaq 100': 'QQQ',
    'Financials': 'XLF',
    'Energy': 'XLE',
    'Healthcare': 'XLV',
    'Industrials': 'XLI',
    'Utilities': 'XLU'
}

@st.cache_data
def assets_to_tickers(assets):
    return [ASSET_DICT[asset] for asset in assets]

st.set_page_config(layout="wide")

col1, col2 = st.columns([1, 2])
assets = col1.multiselect('Assets', list(ASSET_DICT.keys()), default=list(ASSET_DICT.keys()))
col11, col12 = col1.columns(2)

# initialize session state once
if 'start_date' not in st.session_state:
    st.session_state.start_date = '2026-01-01'
if 'end_date' not in st.session_state:
    st.session_state.end_date = 'today'

# dynamic min and max values
start_date = col11.date_input(
    'Start',
    value=st.session_state.start_date,
    max_value=st.session_state.end_date - timedelta(days=1),
    key='start_date'
)
end_date = col12.date_input(
    'End',
    value=st.session_state.end_date,
    min_value=st.session_state.start_date + timedelta(days=1),
    max_value='today',
    key='end_date'
)

tickers = assets_to_tickers(assets)
returns_df = get_returns(tickers, start_date, end_date)
reindexed_prices_df = get_reindexed_prices(tickers, start_date, end_date)

chart_placeholder = col2.container(height=500, border=False)

if 'corr_window' not in st.session_state:
    st.session_state.corr_window = (start_date, end_date)

if st.session_state.corr_window[0] < start_date or st.session_state.corr_window[0] > end_date:
    st.session_state.corr_window = (start_date, st.session_state.corr_window[1])
if st.session_state.corr_window[1] > end_date or st.session_state.corr_window[1] < start_date:
    st.session_state.corr_window = (st.session_state.corr_window[0], end_date)

_, slider_col, _ = col2.columns([5, 130, 1]) # adjust slider width with columns, as there's no width parameter for st.slider()
window_start, window_end = slider_col.slider(
    'Correlation window',
    min_value=start_date,
    max_value=end_date,
    value=(st.session_state.corr_window[0], st.session_state.corr_window[1]),
    format='DD/MM/YYYY',
    key='corr_window'
)

corr = get_correlation(returns_df, window_start, window_end)

fig1 = go.Figure()
for ticker in reindexed_prices_df.columns:
    fig1.add_trace(go.Scatter(x=reindexed_prices_df.index, y=reindexed_prices_df[ticker], mode='lines', name=ticker))
fig1.add_vrect(x0=window_start, x1=window_end, fillcolor='Grey', opacity=0.25, line_width=0)
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
with chart_placeholder:
    st.plotly_chart(fig1, width='stretch')

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
col2.plotly_chart(fig2, width='stretch', theme=None)