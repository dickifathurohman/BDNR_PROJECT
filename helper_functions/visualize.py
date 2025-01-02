import streamlit as st
import pandas as pd
import seaborn as sns
import altair as alt
from connect import *
import time

def bar_chart(data, x_value, y_value, x_title, y_title, selected_data):

    bar_chart = data.groupby(x_value)[y_value].mean().reset_index()
    bar_chart["highlight"] = bar_chart[x_value] == selected_data
    chart = alt.Chart(bar_chart).mark_bar().encode(
        x=alt.X(f"{x_value}:N", sort="-y", title=x_title),
        y=alt.Y(f"{y_value}:Q", title=y_title),
        color=alt.condition(
            alt.datum.highlight,
            alt.value("blue"),
            alt.value("lightblue")
        )
    ).properties(width=800, height=400)
    st.altair_chart(chart, use_container_width=True)

def line_chart(data, x_value, y_value, x_title, y_title, filter_value, selected_data):
    line_chart = data[data[filter_value] == selected_data] if selected_data != "Semua" else data
    line_chart = line_chart.groupby(x_value)[y_value].mean().reset_index()
    line_chart = alt.Chart(line_chart).mark_line().encode(
        x=alt.X(f"{x_value}:O", title=x_title),
        y=alt.Y(f"{y_value}:Q", title=y_title),
        tooltip=[x_value, y_value]
    ).properties(width=400, height=400)
    st.altair_chart(line_chart, use_container_width=True)