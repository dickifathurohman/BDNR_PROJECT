import streamlit as st
import pandas as pd
from connect import *

# Fungsi untuk memuat data dari MongoDB


def load_data():
    cursor = collection.find().sort([("nama_provinsi", 1), ("tahun", 1)])
    data = list(cursor)
    return data

# Sidebar filter untuk provinsi, kota, dan tahun


def sidebar_filters(data, page):
    st.sidebar.title("Filter")

    # Filter provinsi
    provinsi_selected = st.sidebar.selectbox(
        "Pilih Provinsi",
        options=["Semua"] + sorted(list(set(item['nama_provinsi'] for item in data)))
    )

    if page == "Statistik Kemiskinan":
        # Filter kota
        if provinsi_selected == "Semua":
            kota_options = ["Semua"] + sorted(list(
                set(kota['nama_kota']
                    for item in data for kota in item['data_kota'])
            ))
        else:
            kota_options = ["Semua"] + sorted(list(
                set(kota['nama_kota'] for item in data if item['nama_provinsi']
                    == provinsi_selected for kota in item['data_kota'])
            ))

        kota_selected = st.sidebar.selectbox("Pilih Kota", options=kota_options)

    # Filter tahun
    tahun_min, tahun_max = st.sidebar.slider(
        "Filter Rentang Tahun",
        min_value=int(min(item['tahun'] for item in data)),
        max_value=int(max(item['tahun'] for item in data)),
        value=(int(min(item['tahun'] for item in data)),
               int(max(item['tahun'] for item in data)))
    )

    # Filter data berdasarkan provinsi, kota, dan tahun
    filtered_data = [
        item for item in data if item['tahun'] >= tahun_min and item['tahun'] <= tahun_max
    ]

    if page == "Statistik Kemiskinan":
        return filtered_data, provinsi_selected, kota_selected
    else:
        return filtered_data, provinsi_selected

def flatten_data(data, flatten_style='kemiskinan'):
    """
    Jabarkan data kota dari setiap provinsi dan tahun ke dalam daftar datar.
    """
    flattened_data = []
    if flatten_style == 'kemiskinan':
        for item in data:
            for kota in item['data_kota']:
                flattened_data.append({
                    "_id": item["_id"],
                    "tahun": item["tahun"],
                    "nama_provinsi": item["nama_provinsi"],
                    "nama_kota": kota["nama_kota"],
                    "kemiskinan": kota["kemiskinan"],
                })
    elif flatten_style == 'bansos':
        for item in data:
            flattened_data.append({
                "_id": item["_id"],
                "tahun": item["tahun"],
                "nama_provinsi": item["nama_provinsi"],
                "nama_kota": kota["nama_kota"],
                "garis_kemiskinan": kota["kemiskinan"]["garis_kemiskinan"],
                "indeks_kedalaman_kemiskinan": kota["kemiskinan"]["indeks_kedalaman_kemiskinan"],
                "indeks_keparahan_kemiskinan": kota["kemiskinan"]["indeks_keparahan_kemiskinan"],
                "persentase_penduduk_miskin": kota["kemiskinan"]["persentase_penduduk_miskin"],
                "pengeluaran_per_kapita": kota["kemiskinan"]["pengeluaran_per_kapita"],
                "bansos": item["bansos"],
            })
    elif flatten_style == 'tingkat_pengangguran':
        for item in data:
            flattened_data.append({
                "_id": item["_id"],
                "tahun": item["tahun"],
                "nama_provinsi": item["nama_provinsi"],
                "tingkat_pengangguran": item["tingkat_pengangguran"],
            })
    return flattened_data
