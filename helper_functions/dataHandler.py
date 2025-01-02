import streamlit as st
import pandas as pd
from connect import *

# Fungsi untuk memuat data dari MongoDB
def load_data():
    cursor = collection.find().sort([("nama_provinsi", 1), ("tahun", 1)])
    data = list(cursor)
    return data

# Sidebar filter untuk provinsi, kota, dan tahun
def sidebar_filters(data):
    st.sidebar.title("Filter")

    # Filter provinsi
    provinsi_selected = st.sidebar.selectbox(
        "Pilih Provinsi", 
        options=["Semua"] + list(set(item['nama_provinsi'] for item in data))
    )

    # Filter kota
    if provinsi_selected == "Semua":
        kota_options = ["Semua"] + list(
            set(kota['nama_kota'] for item in data for kota in item['data_kota'])
        )
    else:
        kota_options = ["Semua"] + list(
            set(kota['nama_kota'] for item in data if item['nama_provinsi'] == provinsi_selected for kota in item['data_kota'])
        )
    
    kota_selected = st.sidebar.selectbox("Pilih Kota", options=kota_options)

    # Filter tahun
    tahun_min, tahun_max = st.sidebar.slider(
        "Filter Rentang Tahun", 
        min_value=int(min(item['tahun'] for item in data)), 
        max_value=int(max(item['tahun'] for item in data)),
        value=(int(min(item['tahun'] for item in data)), int(max(item['tahun'] for item in data)))
    )

    # Filter data berdasarkan provinsi, kota, dan tahun
    filtered_data = [
        item for item in data if item['tahun'] >= tahun_min and item['tahun'] <= tahun_max
    ]

    return filtered_data, provinsi_selected, kota_selected

def flatten_data(data):
    """
    Jabarkan data kota dari setiap provinsi dan tahun ke dalam daftar datar.
    """
    flattened_data = []
    for item in data:
        for kota in item['data_kota']:
            flattened_data.append({
                "_id"  : item["_id"],
                "tahun": item["tahun"],
                "nama_provinsi": item["nama_provinsi"],
                "nama_kota": kota["nama_kota"],
                "kemiskinan": kota["kemiskinan"]
            })
    return flattened_data