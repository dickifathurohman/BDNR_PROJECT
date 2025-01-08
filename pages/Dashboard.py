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
        
    }
    </style>
    """,
    unsafe_allow_html=True,
)

data = dataHandler.load_data()

filtered_data, provinsi_selected, kota_selected, filtered_data_only_year, tahun_min, tahun_max = dataHandler.sidebar_filters(data, page = "Statistik Kemiskinan")

data_kemiskinan = [
    item for item in filtered_data if 'data_kota' in item and len(item['data_kota']) > 0
]

data_bansos = [
    item for item in filtered_data if 'bansos' in item and bool(item['bansos'])
]

data_pengangguran = [
    item for item in filtered_data if 'tingkat_pengangguran' in item and bool(item['tingkat_pengangguran'])
]

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


#Metrics untuk bansos dan pengangguran
query_filter = {}
if provinsi_selected != "Semua":
    query_filter["nama_provinsi"] = provinsi_selected
query_filter["tahun"] = {"$gte": tahun_min, "$lte": tahun_max}

# Query MongoDB dengan filter
pipeline = [
    {"$match": query_filter},
    {
        "$group": {
            "_id": None,
            "total_rencana_anggaran": {"$sum": "$bansos.rencana_anggaran"},
            "total_realisasi_anggaran": {"$sum": "$bansos.realisasi_anggaran"},
            "total_rencana_penerima": {"$sum": "$bansos.rencana_keluarga_penerima"},
            "total_realisasi_penerima": {"$sum": "$bansos.realisasi_keluarga_penerima"},
            "avg_pengangguran": {"$avg": "$tingkat_pengangguran"}
        }
    }
]

# Eksekusi pipeline
result = list(collection.aggregate(pipeline))

# Ambil hasil total
if result:
    total_rencana_anggaran = result[0]["total_rencana_anggaran"]
    total_realisasi_anggaran = result[0]["total_realisasi_anggaran"]
    total_rencana_penerima = result[0]["total_rencana_penerima"]
    total_realisasi_penerima = result[0]["total_realisasi_penerima"]
    avg_pengangguran = result[0]["avg_pengangguran"]

# Perbedaan dalam Persen
difference_anggaran = (
    (total_realisasi_anggaran - total_rencana_anggaran) / total_rencana_anggaran
) * 100

difference_penerima = (
    (total_realisasi_penerima - total_rencana_penerima) / total_rencana_penerima
) * 100

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        label="Total Rencana Anggaran (Rp)",
        value=f"{total_rencana_anggaran:,.0f}",
    )

with col2:
    st.metric(
        label="Total Realisasi Anggaran (Rp)",
        value=f"{total_realisasi_anggaran:,.0f}",
    )

with col3:
    st.metric(
        label="Perbedaan (%)",
        value=f"{difference_anggaran:.2f}%",
        delta=f"{difference_anggaran:.2f}%",
    )

col4, col5, col6 = st.columns(3)

with col4:
    st.metric(
        label="Total Rencana Keluarga Penerima",
        value=f"{total_rencana_penerima:,.0f}",
    )

with col5:
    st.metric(
        label="Total Realisasi Keluarga Penerima",
        value=f"{total_realisasi_penerima:,.0f}",
    )

with col6:
    st.metric(
        label="Perbedaan (%)",
        value=f"{difference_penerima:.2f}%",
        delta=f"{difference_penerima:.2f}%",
    )

# Metrics untuk kemiskinan
query_filter = {}
if provinsi_selected != "Semua":
    query_filter["nama_provinsi"] = provinsi_selected
if kota_selected != "Semua":
    query_filter["data_kota.nama_kota"] = kota_selected
query_filter["tahun"] = {"$gte": tahun_min, "$lte": tahun_max}

# Pipeline MongoDB untuk menghitung total dan rata-rata kemiskinan
pipeline = [
    {"$match": query_filter},
    {
        "$unwind": "$data_kota"  # Membuka array data_kota
    },
    {"$match": {"data_kota.nama_kota": kota_selected} if kota_selected != "Semua" else {}},  # Filter kota
    {
        "$group": {
            "_id": None,
            "avg_persentase_miskin": {"$avg": "$data_kota.kemiskinan.persentase_penduduk_miskin"},
            "avg_garis_miskin": {"$avg": "$data_kota.kemiskinan.garis_kemiskinan"},
            "avg_pengeluaran_perkapita": {"$avg": "$data_kota.kemiskinan.pengeluaran_per_kapita"},
        }
    }
]

# Eksekusi query
result = list(collection.aggregate(pipeline))

# Menampilkan hasil sebagai metrics
if result:
    avg_persentase_miskin = result[0]["avg_persentase_miskin"]
    avg_garis_miskin = result[0]["avg_garis_miskin"]
    avg_pengeluaran_perkapita = result[0]["avg_pengeluaran_perkapita"]
# Streamlit Layout
col7, col8, col9, col10 = st.columns(4)

with col7:
    st.metric(
        label="Rata-rata Persentase Penduduk Miskin",
        value=f"{avg_persentase_miskin:,.2f}%",
    )

with col8:
    st.metric(
        label="Rata-rata Garis Kemiskinan (Rp)",
        value=f"{avg_garis_miskin:,.0f}",
    )

with col9:
    st.metric(
        label="Rata-rata Pengeluaran Per Kapita (Ribu Rupiah)",
        value=f"{avg_pengeluaran_perkapita:,.0f}",
    )

with col10:
    st.metric(
        label="Rata-rata tingkat pengangguran",
        value=f"{avg_pengangguran:,.2f}",
    )



#Chart
if len(bansos_df) == 0:
    st.warning(f"Tidak ada data Bansos.")
else:

    st.markdown('<p class="custom-font">Anggaran Bantuan Sosial</p>', unsafe_allow_html=True)
    if provinsi_selected == "Semua":
        visualize.dual_bar_chart(bansos_df, "nama_provinsi", "rencana_anggaran", "realisasi_anggaran", "Jumlah Anggaran")
        visualize.dual_line_chart(bansos_df, "tahun", "rencana_anggaran", "realisasi_anggaran", "Jumlah Anggaran")
    else:
        col1, col2 = st.columns(2)

        with col1:
            visualize.dual_bar_chart(bansos_df, "nama_provinsi", "rencana_anggaran", "realisasi_anggaran", "Jumlah Anggaran")
        with col2:
            visualize.dual_line_chart(bansos_df, "tahun", "rencana_anggaran", "realisasi_anggaran", "Jumlah Anggaran")

    st.markdown('<p class="custom-font">Jumlah Penerima Bantuan Sosial</p>', unsafe_allow_html=True)
    if provinsi_selected == "Semua":
        visualize.dual_bar_chart(bansos_df, "nama_provinsi", "rencana_keluarga_penerima", "realisasi_keluarga_penerima", "Jumlah Penerima")
        visualize.dual_line_chart(bansos_df, "tahun", "rencana_keluarga_penerima", "realisasi_keluarga_penerima", "Jumlah Penerima")
    else:
        col1, col2 = st.columns(2)

        with col1:
            visualize.dual_bar_chart(bansos_df, "nama_provinsi", "rencana_keluarga_penerima", "realisasi_keluarga_penerima", "Jumlah Penerima")
        with col2:
            visualize.dual_line_chart(bansos_df, "tahun", "rencana_keluarga_penerima", "realisasi_keluarga_penerima", "Jumlah Penerima")

#col1, col2 = st.columns([2, 2])

if len(kemiskinan_df) == 0:
    st.warning(f"Tidak ada data statistik kemiskinan.")
else:
    col1, col2 = st.columns(2)
    with col1:
        if provinsi_selected == "Semua":
            st.markdown('<p class="custom-font">Persentase Penduduk Miskin</p>', unsafe_allow_html=True)
            visualize.bar_chart(kemiskinan_df, "nama_provinsi", "persentase_penduduk_miskin", "Provinsi", "Persentase Penduduk Miskin (%)", provinsi_selected)
        else: 
            if len(kemiskinan_df) == 0:
                # Jika tidak ada data kota untuk provinsi yang dipilih
                st.warning(f"Tidak ada data kota untuk provinsi { dataHandler.title_case(provinsi_selected) }.")
            else:
                if kota_selected == "Semua":
                    st.markdown(f'<p class="custom-font">Persentase Penduduk Miskin {dataHandler.title_case(provinsi_selected)}</p>', unsafe_allow_html=True)
                    visualize.bar_chart(kemiskinan_df, "nama_kota", "persentase_penduduk_miskin", "Kabupaten / Kota", "Persentase Penduduk Miskin (%)", kota_selected)
                else:
                    st.markdown(f'<p class="custom-font">Persentase Penduduk Miskin {dataHandler.title_case(provinsi_selected)}</p>', unsafe_allow_html=True)
                    visualize.bar_chart(kemiskinan_df, "nama_kota", "persentase_penduduk_miskin", "Kabupaten / Kota", "Persentase Penduduk Miskin (%)", kota_selected, filter_kota=True)

    with col2:
        if provinsi_selected == "Semua":
            st.markdown('<p class="custom-font">Trend Persentase Penduduk Miskin</p>', unsafe_allow_html=True)
            visualize.line_chart(kemiskinan_df, "tahun", "persentase_penduduk_miskin", "Tahun", "Persentase Penduduk Miskin (%)", "nama_provinsi", provinsi_selected)

        else:
            if len(kemiskinan_df) == 0:
                # Jika tidak ada data kota untuk provinsi yang dipilih
                st.warning(f"Tidak ada data kota untuk provinsi {dataHandler.title_case(provinsi_selected)}.")
            else:

                if kota_selected == "Semua":
                    st.markdown(f'<p class="custom-font">Trend Persentase Penduduk Miskin {dataHandler.title_case(provinsi_selected)}</p>', unsafe_allow_html=True)
                    visualize.line_chart(kemiskinan_df, "tahun", "persentase_penduduk_miskin", "Tahun", "Persentase Penduduk Miskin (%)", "nama_provinsi", provinsi_selected, "filtered_prov", kemiskinan_df_full)
                else:
                    st.markdown(f'<p class="custom-font">Trend Persentase Penduduk Miskin {dataHandler.title_case(kota_selected)}</p>', unsafe_allow_html=True)
                    visualize.line_chart(kemiskinan_df, "tahun", "persentase_penduduk_miskin", "Tahun", "Persentase Penduduk Miskin (%)", "nama_kota", kota_selected, "filtered_kota", kemiskinan_df_full, provinsi_selected)

    col3, col4 = st.columns(2)

    with col3:
        if provinsi_selected == "Semua":
            st.markdown('<p class="custom-font">Garis Kemiskinan</p>', unsafe_allow_html=True)
            visualize.bar_chart(kemiskinan_df, "nama_provinsi", "garis_kemiskinan", "Provinsi", "Garis Kemiskinan (rupiah/kapita/bulan)", provinsi_selected)
        else: 
            if len(kemiskinan_df) == 0:
                # Jika tidak ada data kota untuk provinsi yang dipilih
                st.warning(f"Tidak ada data kota untuk provinsi { dataHandler.title_case(provinsi_selected) }.")
            else:
                if kota_selected == "Semua":
                    st.markdown(f'<p class="custom-font">Garis Kemiskinan {dataHandler.title_case(provinsi_selected)}</p>', unsafe_allow_html=True)
                    visualize.bar_chart(kemiskinan_df, "nama_kota", "garis_kemiskinan", "Kabupaten / Kota", "Garis Kemiskinan (rupiah/kapita/bulan)", kota_selected)
                else:
                    st.markdown(f'<p class="custom-font">Garis Kemiskinan {dataHandler.title_case(provinsi_selected)}</p>', unsafe_allow_html=True)
                    visualize.bar_chart(kemiskinan_df, "nama_kota", "garis_kemiskinan", "Kabupaten / Kota", "Garis Kemiskinan (rupiah/kapita/bulan)", kota_selected, filter_kota=True)

    with col4:
        if provinsi_selected == "Semua":
            st.markdown('<p class="custom-font">Trend Garis Kemiskinan</p>', unsafe_allow_html=True)
            visualize.line_chart(kemiskinan_df, "tahun", "garis_kemiskinan", "Tahun", "Garis Kemiskinan (rupiah/kapita/bulan)", "nama_provinsi", provinsi_selected)

        else:
            if len(kemiskinan_df) == 0:
                # Jika tidak ada data kota untuk provinsi yang dipilih
                st.warning(f"Tidak ada data kota untuk provinsi {dataHandler.title_case(provinsi_selected)}.")
            else:

                if kota_selected == "Semua":
                    st.markdown(f'<p class="custom-font">Trend Garis Kemiskinan {dataHandler.title_case(provinsi_selected)}</p>', unsafe_allow_html=True)
                    visualize.line_chart(kemiskinan_df, "tahun", "garis_kemiskinan", "Tahun", "Garis Kemiskinan (rupiah/kapita/bulan)", "nama_provinsi", provinsi_selected, "filtered_prov", kemiskinan_df_full)
                else:
                    st.markdown(f'<p class="custom-font">Trend Garis Kemiskinan {dataHandler.title_case(kota_selected)}</p>', unsafe_allow_html=True)
                    visualize.line_chart(kemiskinan_df, "tahun", "garis_kemiskinan", "Tahun", "Garis Kemiskinan (rupiah/kapita/bulan)", "nama_kota", kota_selected, "filtered_kota", kemiskinan_df_full, provinsi_selected)

    col5, col6 = st.columns(2)

    with col5:
        if provinsi_selected == "Semua":
            st.markdown('<p class="custom-font">Pengeluaran per Kapita</p>', unsafe_allow_html=True)
            visualize.bar_chart(kemiskinan_df, "nama_provinsi", "pengeluaran_per_kapita", "Provinsi", "Pengeluaran per Kapita (ribu rupiah/orang/tahun)", provinsi_selected)
        else: 
            if len(kemiskinan_df) == 0:
                # Jika tidak ada data kota untuk provinsi yang dipilih
                st.warning(f"Tidak ada data kota untuk provinsi { dataHandler.title_case(provinsi_selected) }.")
            else:
                if kota_selected == "Semua":
                    st.markdown(f'<p class="custom-font">Pengeluaran per Kapita {dataHandler.title_case(provinsi_selected)}</p>', unsafe_allow_html=True)
                    visualize.bar_chart(kemiskinan_df, "nama_kota", "pengeluaran_per_kapita", "Kabupaten / Kota", "Pengeluaran per Kapita (ribu rupiah/orang/tahun)", kota_selected)
                else:
                    st.markdown(f'<p class="custom-font">Pengeluaran per Kapita {dataHandler.title_case(provinsi_selected)}</p>', unsafe_allow_html=True)
                    visualize.bar_chart(kemiskinan_df, "nama_kota", "pengeluaran_per_kapita", "Kabupaten / Kota", "Pengeluaran per Kapita (ribu rupiah/orang/tahun)", kota_selected, filter_kota=True)

    with col6:
        if provinsi_selected == "Semua":
            st.markdown('<p class="custom-font">Trend Pengeluaran per Kapita</p>', unsafe_allow_html=True)
            visualize.line_chart(kemiskinan_df, "tahun", "pengeluaran_per_kapita", "Tahun", "Pengeluaran per Kapita (ribu rupiah/orang/tahun)", "nama_provinsi", provinsi_selected)

        else:
            if len(kemiskinan_df) == 0:
                # Jika tidak ada data kota untuk provinsi yang dipilih
                st.warning(f"Tidak ada data kota untuk provinsi {dataHandler.title_case(provinsi_selected)}.")
            else:

                if kota_selected == "Semua":
                    st.markdown(f'<p class="custom-font">Trend Pengeluaran per Kapita {dataHandler.title_case(provinsi_selected)}</p>', unsafe_allow_html=True)
                    visualize.line_chart(kemiskinan_df, "tahun", "pengeluaran_per_kapita", "Tahun", "Pengeluaran per Kapita (ribu rupiah/orang/tahun)", "nama_provinsi", provinsi_selected, "filtered_prov", kemiskinan_df_full)
                else:
                    st.markdown(f'<p class="custom-font">Trend Pengeluaran per Kapita {dataHandler.title_case(kota_selected)}</p>', unsafe_allow_html=True)
                    visualize.line_chart(kemiskinan_df, "tahun", "pengeluaran_per_kapita", "Tahun", "Pengeluaran per Kapita (ribu rupiah/orang/tahun)", "nama_kota", kota_selected, "filtered_kota", kemiskinan_df_full, provinsi_selected)

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
