import streamlit as st
import pandas as pd
import seaborn as sns
import altair as alt
from connect import *
import time
from helper_functions import dataHandler, visualize

st.set_page_config(layout="wide")  
st.title("Dashboard Visualizations")

# Tambahkan CSS kustom buat title chart
st.markdown(
    """
    <style>
    .custom-font {
        font-size: 18px !important;
        font-weight: bold;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

data = dataHandler.load_data()

filtered_data, provinsi_selected, kota_selected, filtered_data_only_year = dataHandler.sidebar_filters(data, page = "Statistik Kemiskinan")

data_kemiskinan = [
    item for item in filtered_data if 'data_kota' in item and len(item['data_kota']) > 0
]

data_bansos = [
    item for item in filtered_data if 'bansos' in item and bool(item['bansos'])
]

data_pengangguran = [
    item for item in filtered_data if 'tingkat_pengangguran' in item and bool(item['tingkat_pengangguran'])
]

# Ambil data berdasarkan provinsi dan kota yang dipilih
#if provinsi_selected != "Semua":
#    data_kemiskinan = [item for item in data_kemiskinan if item['nama_provinsi'] == provinsi_selected]
#    data_bansos = [item for item in data_bansos if item['nama_provinsi'] == provinsi_selected]

kemiskinan_flattened = dataHandler.flatten_data(data_kemiskinan)
kemiskinan_df = pd.DataFrame(kemiskinan_flattened)

# Data kemiskinan full
kemiskinan_flattened_full = dataHandler.flatten_data(filtered_data_only_year)
kemiskinan_df_full = pd.DataFrame(kemiskinan_flattened_full)

bansos_flattened = dataHandler.flatten_data(data_bansos, flatten_style='bansos')
bansos_df = pd.DataFrame(bansos_flattened)

# Data tingkat pengangguran yang sudah di-filter
pengangguran_flattened = dataHandler.flatten_data(data_pengangguran, flatten_style='tingkat_pengangguran')
pengangguran_df = pd.DataFrame(pengangguran_flattened)

# Data tingkat pengangguran full
pengangguran_flattened_full = dataHandler.flatten_data(filtered_data_only_year, flatten_style='tingkat_pengangguran')
pengangguran_df_full = pd.DataFrame(pengangguran_flattened_full)

col1, col2 = st.columns([2, 2])

if len(kemiskinan_df) == 0:
    st.warning(f"Tidak ada data statistik kemiskinan.")
else:
    with col1:
        if provinsi_selected == "Semua":
            st.markdown('<p class="custom-font">Persentase Penduduk Miskin</p>', unsafe_allow_html=True)
            visualize.bar_chart(kemiskinan_df, "nama_provinsi", "persentase_penduduk_miskin", "Provinsi", "Persentase Penduduk Miskin", provinsi_selected)
        else: 
            if len(kemiskinan_df) == 0:
                # Jika tidak ada data kota untuk provinsi yang dipilih
                st.warning(f"Tidak ada data kota untuk provinsi { dataHandler.title_case(provinsi_selected) }.")
            else:
                if kota_selected == "Semua":
                    st.markdown(f'<p class="custom-font">Persentase Penduduk Miskin {dataHandler.title_case(provinsi_selected)}</p>', unsafe_allow_html=True)
                    visualize.bar_chart(kemiskinan_df, "nama_kota", "persentase_penduduk_miskin", "Kabupaten / Kota", "Persentase Penduduk Miskin", kota_selected)
                else:
                    st.markdown(f'<p class="custom-font">Persentase Penduduk Miskin {dataHandler.title_case(provinsi_selected)}</p>', unsafe_allow_html=True)
                    visualize.bar_chart(kemiskinan_df, "nama_kota", "persentase_penduduk_miskin", "Kabupaten / Kota", "Persentase Penduduk Miskin", kota_selected, filter_kota=True)


    with col2:
        if provinsi_selected == "Semua":
            st.markdown('<p class="custom-font">Trend Persentase Penduduk Miskin</p>', unsafe_allow_html=True)
            visualize.line_chart(kemiskinan_df, "tahun", "persentase_penduduk_miskin", "Tahun", "Persentase Penduduk Miskin", "nama_provinsi", provinsi_selected)

        else:
            if len(kemiskinan_df) == 0:
                # Jika tidak ada data kota untuk provinsi yang dipilih
                st.warning(f"Tidak ada data kota untuk provinsi {dataHandler.title_case(provinsi_selected)}.")
            else:

                if kota_selected == "Semua":
                    st.markdown(f'<p class="custom-font">Trend Persentase Penduduk Miskin {dataHandler.title_case(provinsi_selected)}</p>', unsafe_allow_html=True)
                    visualize.line_chart(kemiskinan_df, "tahun", "persentase_penduduk_miskin", "Tahun", "Persentase Penduduk Miskin", "nama_provinsi", provinsi_selected, "filtered_prov", kemiskinan_df_full)
                else:
                    st.markdown(f'<p class="custom-font">Trend Persentase Penduduk Miskin {dataHandler.title_case(kota_selected)}</p>', unsafe_allow_html=True)
                    visualize.line_chart(kemiskinan_df, "tahun", "persentase_penduduk_miskin", "Tahun", "Persentase Penduduk Miskin", "nama_kota", kota_selected, "filtered_kota", kemiskinan_df_full, provinsi_selected)

if len(bansos_df) == 0:
    st.warning(f"Tidak ada data Bansos.")
else:
    if provinsi_selected == "Semua":
        visualize.dual_bar_chart(bansos_df, "nama_provinsi", "rencana_anggaran", "realisasi_anggaran", "Jumlah Anggaran")
        visualize.dual_line_chart(bansos_df, "tahun", "rencana_anggaran", "realisasi_anggaran", "Jumlah Anggaran")
    else:
        col1, col2 = st.columns(2)

        with col1:
            visualize.dual_bar_chart(bansos_df, "nama_provinsi", "rencana_anggaran", "realisasi_anggaran", "Jumlah Anggaran")
        with col2:
            visualize.dual_line_chart(bansos_df, "tahun", "rencana_anggaran", "realisasi_anggaran", "Jumlah Anggaran")

if len(pengangguran_df) == 0:
    st.warning(f"Tidak ada data Bansos.")
else:
    col5, col6 = st.columns(2)
    with col5:
        if provinsi_selected == "Semua":
            st.markdown('<p class="custom-font">Rata-Rata Tingkat Pengangguran</p>', unsafe_allow_html=True)
            
            visualize.bar_chart(pengangguran_df, "nama_provinsi", "tingkat_pengangguran", "Provinsi", "Tingkat Pengangguran", provinsi_selected)
        else:
            st.markdown(f'<p class="custom-font">Rata-Rata Tingkat Pengangguran {dataHandler.title_case(provinsi_selected)}</p>', unsafe_allow_html=True)

            visualize.bar_chart(pengangguran_df, "nama_provinsi", "tingkat_pengangguran", "Provinsi", "Tingkat Pengangguran", "Se-Indonesia", "tingpeng", pengangguran_df_full)
    with col6:
        if provinsi_selected == "Semua":
            st.markdown('<p class="custom-font">Trend Tingkat Pengangguran</p>', unsafe_allow_html=True)
            visualize.line_chart(pengangguran_df, "tahun", "tingkat_pengangguran", "Tahun", "Persentase Penduduk Miskin", "nama_provinsi", provinsi_selected)
        else:
            if len(kemiskinan_df) == 0:
                # Jika tidak ada data kota untuk provinsi yang dipilih
                st.warning(f"Tidak ada data kota untuk provinsi {dataHandler.title_case(provinsi_selected)}.")
            else:
                st.markdown(f'<p class="custom-font">Trend Tingkat Pengangguran {dataHandler.title_case(provinsi_selected)}</p>', unsafe_allow_html=True)
                
                visualize.line_chart(pengangguran_df, "tahun", "tingkat_pengangguran", "Tahun", "Tingkat Pengangguran (%)", "nama_provinsi", provinsi_selected, "filtered_prov", pengangguran_df_full)

    st.markdown('<p class="custom-font">Trend Tingkat Pengangguran Seluruh Indonesia</p>', unsafe_allow_html=True)
    
    visualize.choropleth_chart(pengangguran_df_full, "nama_provinsi", "tingkat_pengangguran", "Nama Provinsi", "Tingkat Pengangguran")
