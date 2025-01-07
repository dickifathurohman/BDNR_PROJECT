import streamlit as st
import pandas as pd
import seaborn as sns
import altair as alt
import plotly.express as px
import requests
import json
from connect import *
import time
from helper_functions import dataHandler

def bar_chart(data, x_value, y_value, x_title, y_title, selected_data, jenis="bukan_tingpeng", data_full="_", filter_kota=False):
    bar_chart = data.groupby(x_value)[y_value].mean().reset_index()
    if jenis == "tingpeng":
        # Hitung rata-rata tingkat pengangguran per tahun
        average_pengangguran = data_full.groupby('tahun')['tingkat_pengangguran'].mean().reset_index()
        
        # Tambahkan kolom nama_provinsi dengan nilai "Se-Indonesia"
        average_pengangguran['nama_provinsi'] = 'Se-Indonesia'

        # Hitung rata-rata seluruh Indonesia
        average_pengangguran = average_pengangguran.groupby('nama_provinsi')['tingkat_pengangguran'].mean().reset_index()
        
        # Gabungkan dengan data asli
        bar_chart = pd.concat([bar_chart, average_pengangguran], ignore_index=True)

    if filter_kota:
        bar_chart["highlight"] = bar_chart[x_value] == selected_data
    else:
        max_value = bar_chart[y_value].max()
        bar_chart["highlight"] = bar_chart[y_value] == max_value
    chart = alt.Chart(bar_chart).mark_bar().encode(
        x=alt.X(f"{x_value}:N", sort="-y", title=x_title),
        y=alt.Y(f"{y_value}:Q", title=y_title),
        color=alt.condition(
            alt.datum.highlight,
            alt.value("#3d7bba"),
            alt.value("#bed5ea"),
        )
    ).properties(width=800, height=400)
    
    st.altair_chart(chart, use_container_width=True)
        

def line_chart(data, x_value, y_value, x_title, y_title, filter_value, selected_data, filtered="bukan_filtered", data_full="_", prov="_"):
    line_chart = data[data[filter_value] == selected_data] if selected_data != "Semua" else data
    
    line_chart = line_chart.groupby(x_value)[y_value].mean().reset_index()
    
    if filtered == "filtered_prov" or filtered == "filtered_kota":
        if filtered == "filtered_prov":
            line_chart[filter_value] = dataHandler.title_case(selected_data)
        else:
            line_chart[filter_value] = dataHandler.title_case(selected_data)
            data_full = data_full[data_full['nama_provinsi'] == prov]

        # Hitung rata-rata tingkat pengangguran per tahun
        average_all = data_full.groupby(x_value)[y_value].mean().reset_index()
        
        # Tambahkan kolom nama_provinsi dengan kategori di atasnya 1 : misal data di filter per-provinsi, maka 1 kategori di atasnya adalah Se-Indonesia
        if filtered == "filtered_prov":
            average_all[filter_value] = 'Se-Indonesia'
        else:
            average_all[filter_value] = dataHandler.title_case(prov)
        
        # Gabungkan dengan data asli
        line_chart = pd.concat([line_chart, average_all], ignore_index=True)

        line_chart = alt.Chart(line_chart).mark_line().encode(
            x=alt.X(f"{x_value}:O", title=x_title),
            y=alt.Y(f"{y_value}:Q", title=y_title),
            color=alt.Color(f'{filter_value}:N', legend=alt.Legend(title="Nama Provinsi", orient='bottom')),
            tooltip=[x_value, filter_value, y_value]
        ).properties(
            width=800,
            height=400,
        )
    else:
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
    
    # Membuat bar chart dengan Altair    
    dual_bar_chart = alt.Chart(chart_data).mark_bar().encode(    
        x=alt.X(f'{x_value}:N', sort=None, title='Nama Provinsi'),    
        y=alt.Y(f'{value_name}:Q', title='Jumlah Anggaran'),    
        color=alt.Color('Kategori:N', legend=alt.Legend(title='Kategori', orient='bottom')),
        # Menggunakan xOffset untuk memisahkan bar    
        xOffset=alt.X('Kategori:N', title=None)    
    ).properties(    
        width=150,  # Lebar setiap bar    
        height=400  # Tinggi chart    
    ) 

    st.altair_chart(dual_bar_chart, use_container_width=True)


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
    
    dual_line_chart = alt.Chart(chart_data).mark_line().encode(
        x=alt.X(f"{x_value}:O", title="Tahun"),
        y=alt.Y(f"{value_name}:Q", title="Jumlah Anggaran"),
        color=alt.Color('Kategori:N', legend=alt.Legend(title="Kategori", orient='bottom')),
        tooltip=[x_value, 'Kategori', value_name]
    ).properties(
        width=800,
        height=400,
    )

    st.altair_chart(dual_line_chart, use_container_width=True)

def choropleth_chart(data, x_value, y_value):
    # Aggregating data berdsarakan provinsi
    data_aggregated = data.groupby(x_value)[y_value].mean().reset_index()

    # Menyesuaikan dengan data GeoJSON
    # Mengubah nama_provinsi menjadi title case  
    data_aggregated['nama_provinsi'] = data_aggregated['nama_provinsi'].str.title()

    # Mengubah nama provinsi  
    data_aggregated['nama_provinsi'] = data_aggregated['nama_provinsi'].replace({  
        "Dki Jakarta": "Jakarta Raya",
        "Kepulauan Bangka Belitung": "Bangka-Belitung",
        "Di Yogyakarta": "Yogyakarta"
    })

    geojson_url = "https://raw.githubusercontent.com/superpikar/indonesia-geojson/master/indonesia.geojson"
    response = requests.get(geojson_url)
    geojson_data = response.json()  # Mengonversi response ke format JSON

    # Membuat choropleth map
    fig = px.choropleth(
        data_aggregated,
        geojson=geojson_data,
        locations=x_value,
        featureidkey='properties.state',  # Sesuaikan dengan nama properti di GeoJSON
        color=y_value,
        hover_name=x_value,
        color_continuous_scale=px.colors.sequential.Blues,
        title='Tingkat Pengangguran di Indonesia',
        width=700,
        height=700
    )

    # Menambahkan layout untuk peta
    fig.update_geos(
        fitbounds="locations", 
        visible=False, 
        bgcolor='#ffffff',  # Mengatur latar belakang peta menjadi transparan
        # landcolor='blue',  # Mengatur warna daratan menjadi transparan
        # bgcolor='rgba(0,0,0,0)',
    )

    # Mengatur posisi judul
    fig.update_layout(title_y=0.87)

    # Menampilkan di Streamlit
    st.plotly_chart(fig, use_container_width=True)