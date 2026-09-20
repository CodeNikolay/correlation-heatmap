import datetime as dt
import plotly.graph_objs as go
import pandas as pd

from data_loader import *
from correlations import get_correlation

ASSETS = [('SPY', 0), ('QQQ', 0), ('XLF', 0), ('XLE', 0), ('XLV', 0), ('XLI', 0), ('XLU', 0)]

# initialize persistent state for custom assets
if "custom_assets_names" not in st.session_state:
    st.session_state.custom_assets_names = []

if "custom_assets_df" not in st.session_state:
    st.session_state.custom_assets_df = pd.DataFrame()

def add_custom_asset():
    """Process the newly uploaded asset."""
    new_asset = st.session_state.new_asset
    name = st.session_state.new_asset_name

    if new_asset is None or not name:
        return

    new_asset_df = pd.read_csv(new_asset, index_col='Date', sep=';')
    new_asset_df.rename(
        columns={new_asset_df.columns[0]: name},
        inplace=True
    )
    new_asset_df.index = pd.to_datetime(new_asset_df.index)
    if new_asset_df[name].dtype == 'str':
        new_asset_df[name] = (
            new_asset_df[name]
            .str.replace('$', '', regex=False)
            .astype(float)
        )
    else:
        new_asset_df[name] = new_asset_df[name].astype(float)

    st.session_state.custom_assets_names.append((name, 1))

    st.session_state.custom_assets_df = (
        st.session_state.custom_assets_df.join(
            new_asset_df,
            how="outer"
        )
    )

st.set_page_config(layout="wide")

col1, col2 = st.columns([1, 2])

if "assets" not in st.session_state:
    st.session_state.assets = ASSETS + st.session_state.custom_assets_names

assets = col1.multiselect(
    'Assets',
    ASSETS + st.session_state.custom_assets_names,
    format_func=lambda x: x[0],
    default=st.session_state.assets
)

if not assets:
    col1.warning("Please select at least one asset.")
    st.stop()

# initialize session state once for correlation window
if 'start_date' not in st.session_state:
    st.session_state.start_date = dt.date.fromisoformat('2026-01-01')
if 'end_date' not in st.session_state:
    st.session_state.end_date = dt.date.today()

# dynamic min and max values
col11, col12 = col1.columns(2)
start_date = col11.date_input(
    label='Start',
    value=st.session_state.start_date,
    max_value=st.session_state.end_date - dt.timedelta(days=1),
    key='start_date'
)
end_date = col12.date_input(
    label='End',
    value=st.session_state.end_date,
    min_value=st.session_state.start_date + dt.timedelta(days=1),
    max_value='today',
    key='end_date'
)

with col1.container(border=True):
    st.markdown("#### Add new asset")

    new_asset_name = st.text_input(
        "Name of new asset",
        key="new_asset_name"
    )

    if new_asset_name:
        new_asset = st.file_uploader(
            "Upload asset file",
            type="csv",
            key="new_asset",
            on_change=add_custom_asset
        )
    else:
        st.empty()

# reserve space for assets history chart
chart_placeholder = col2.container(height=500, border=False)

# initialize correlation window with full history window
if 'corr_window' not in st.session_state:
    st.session_state.corr_window = (start_date, end_date)

# constraints for correlation window
if st.session_state.corr_window[0] < start_date or st.session_state.corr_window[0] > end_date:
    st.session_state.corr_window = (start_date, st.session_state.corr_window[1])
if st.session_state.corr_window[1] > end_date or st.session_state.corr_window[1] < start_date:
    st.session_state.corr_window = (st.session_state.corr_window[0], end_date)

# correlation window slider
_, slider_col, _ = col2.columns([5, 130, 1]) # adjust slider width with columns, as there's no width parameter for st.slider()
window_start, window_end = slider_col.slider(
    'Correlation window',
    min_value=start_date,
    max_value=end_date,
    value=(st.session_state.corr_window[0], st.session_state.corr_window[1]),
    format='DD/MM/YYYY',
    key='corr_window'
)

# get assets history, returns and correlation
selected_tickers = [x[0] for x in assets if not x[1]]
selected_custom_assets = [x[0] for x in assets if x[1]]

tickers_prices_df = get_prices(selected_tickers, start_date, end_date)
custom_prices_df = st.session_state.custom_assets_df[selected_custom_assets]
custom_prices_df = custom_prices_df.loc[start_date:end_date]
prices_df = tickers_prices_df.join(custom_prices_df, how='outer')

returns_df = prices_to_returns(prices_df)

reindexed_prices_df = get_reindexed_prices(prices_df)

corr = get_correlation(returns_df, window_start, window_end)

# assets history chart
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

# correlation heatmap
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