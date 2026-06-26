import matplotlib.pyplot as plt
import streamlit as st
import plotly.graph_objs as go

st.text_input('Assets')
fig = go.Figure(data=go.Heatmap())
