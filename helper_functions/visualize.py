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

def dual_bar_chart(data, x_value, value1, value2, value_name):

    aggregated_data = data.groupby([x_value], as_index=False).agg(
        {value1: 'sum', value2: 'sum'}  # Bisa diganti 'mean' jika ingin rata-rata
    )

    chart_data = aggregated_data.melt(
        id_vars=[x_value],
        value_vars=[value1, value2],
        var_name="Kategori",
        value_name=value_name,
        )

    st.bar_chart(chart_data, x=x_value, y=value_name, color="Kategori", stack=False)


def dual_line_chart(data, x_value, value1, value2, value_name):

    aggregated_data = data.groupby([x_value], as_index=False).agg(
        {value1: 'sum', value2: 'sum'}  # Bisa diganti 'mean' jika ingin rata-rata
    )

    aggregated_data[x_value] = aggregated_data[x_value].astype(int)

    chart_data = aggregated_data.melt(
        id_vars=[x_value],
        value_vars=[value1, value2],
        var_name="Kategori",
        value_name=value_name,
        )

    st.line_chart(chart_data, x=x_value, y=value_name, color="Kategori")