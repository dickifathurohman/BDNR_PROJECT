import streamlit as st
import pandas as pd
import seaborn as sns
import altair as alt
from connect import *
import time
from helper_functions import dataHandler, visualize

st.set_page_config(layout="wide")  
st.title("Dashboard Visualizations")

data = dataHandler.load_data()

filtered_data, provinsi_selected, kota_selected = dataHandler.sidebar_filters(data)

data_kemiskinan = [
    item for item in filtered_data if 'data_kota' in item and len(item['data_kota']) > 0
]

# Ambil data berdasarkan provinsi dan kota yang dipilih
if provinsi_selected != "Semua":
    data_kemiskinan = [item for item in data_kemiskinan if item['nama_provinsi'] == provinsi_selected]


kemiskinan_flattened = dataHandler.flatten_data(data_kemiskinan)
kemiskinan_df = pd.DataFrame(kemiskinan_flattened)

col1, col2 = st.columns(2)

with col1:
    if provinsi_selected == "Semua":

        st.subheader("Persentase Penduduk Miskin")
        visualize.bar_chart(kemiskinan_df, "nama_provinsi", "persentase_penduduk_miskin", "Provinsi", "Persentase Penduduk Miskin", provinsi_selected)
    else: 

        if len(kemiskinan_df) == 0:
            # Jika tidak ada data kota untuk provinsi yang dipilih
            st.warning(f"Tidak ada data kota untuk provinsi {provinsi_selected}.")
        else:
            st.subheader(f"Persentase Penduduk Miskin {provinsi_selected}")
            visualize.bar_chart(kemiskinan_df, "nama_kota", "persentase_penduduk_miskin", "Kabupaten / Kota", "Persentase Penduduk Miskin", kota_selected)

with col2:
    if provinsi_selected == "Semua":
        st.subheader("Trend Persentase Penduduk Miskin")
        visualize.line_chart(kemiskinan_df, "tahun", "persentase_penduduk_miskin", "Tahun", "Persentase Penduduk Miskin", "nama_provinsi", provinsi_selected)

    else:
        if len(kemiskinan_df) == 0:
            # Jika tidak ada data kota untuk provinsi yang dipilih
            st.warning(f"Tidak ada data kota untuk provinsi {provinsi_selected}.")
        else:
            st.subheader(f"Trend Persentase Penduduk Miskin {provinsi_selected}")
            visualize.line_chart(kemiskinan_df, "tahun", "persentase_penduduk_miskin", "Tahun", "Persentase Penduduk Miskin", "nama_kota", kota_selected)

filtered_data, provinsi_selected, kota_selected = dataHandler.sidebar_filters(data, page = "Statistik Kemiskinan")
