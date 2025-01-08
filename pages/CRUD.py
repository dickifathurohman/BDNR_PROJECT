import streamlit as st
import pandas as pd
import altair as alt
from connect import *
import time
from helper_functions import dataHandler, crud

# Untuk mengelola jumlah data per halaman
def get_paginated_data(data, page_num, page_size):
    start = page_num * page_size
    end = start + page_size
    return data[start:end]


def update_kota():
    st.session_state.selected_kota = None


st.set_page_config(layout="wide")
st.title("CRUD Operations")
page = st.selectbox("Pilih Data", [
                    "Statistik Kemiskinan", "Bantuan Sosial Pangan", "Tingkat Pengangguran"])
data = dataHandler.load_data()

if page == "Statistik Kemiskinan":

    st.header("Data Statistik Kemiskinan")

    # get data
    filtered_data, provinsi_selected, kota_selected, X, _, _ = dataHandler.sidebar_filters(
        data, page)

    filtered_data = [
        item for item in filtered_data if 'data_kota' in item and len(item['data_kota']) > 0
    ]

    if kota_selected != "Semua":
        filtered_data = [
            {
                **item,
                "data_kota": [
                    kota for kota in item['data_kota'] if kota['nama_kota'] == kota_selected
                ]
            }
            for item in filtered_data
            if any(kota['nama_kota'] == kota_selected for kota in item['data_kota'])
        ]

    st.subheader("Tambah Data Statistik Kemiskinan")

    # Inisialisasi session_state untuk provinsi dan kota
    if "selected_provinsi" not in st.session_state:
        st.session_state.selected_provinsi = None
    if "selected_kota" not in st.session_state:
        st.session_state.selected_kota = None

    col1, col2 = st.columns(2)

    with col1:
        # Pilihan Provinsi
        provinsi_options = ["Pilih Provinsi"] + sorted(list(set(item["nama_provinsi"] for item in data)))
        provinsi = st.selectbox(
            "Pilih Provinsi",
            options=provinsi_options,
            key="selected_provinsi",
        )
    with col2:

        # Pilihan Kota
        if st.session_state.selected_provinsi and st.session_state.selected_provinsi != "Pilih Provinsi":
            kota_options = sorted(list(
                set(
                    kota["nama_kota"]
                    for item in data
                    if item["nama_provinsi"] == st.session_state.selected_provinsi
                    for kota in item["data_kota"]
                )
            ))
            kota = st.selectbox(
                "Pilih Kota",
                options=kota_options,
                key="selected_kota",
            )
        else:
            # Jika provinsi belum dipilih dropdown kota dalam keadaan disabled
            kota = st.selectbox(
                "Pilih Kota",
                options=["Silakan pilih provinsi terlebih dahulu"],
                disabled=True,  # Menjadikan dropdown disabled
                key="disabled_kota",
            )

    # Form untuk Submit Data
    with st.form("add_data_form"):

        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)
        col5, col6 = st.columns(2)

        with col1:
            tahun = st.number_input(
                "Tahun", min_value=2000, max_value=2100, step=1)
        with col2:
            ppm = st.number_input("Persentase Penduduk Miskin")
        with col3:
            ikk = st.number_input("Indeks Kedalaman Kemiskinan")
        with col4:
            ipk = st.number_input("Indeks Keparahan Kemiskinan")
        with col5:
            gk = st.number_input("Garis Kemiskinan")
        with col6:
            ppk = st.number_input("Pengeluaran per Kapita")

        submitted = st.form_submit_button("Submit")
        if submitted:
            if st.session_state.selected_provinsi and st.session_state.selected_kota:
                crud.add_kemiskinan(tahun, provinsi, kota,
                                    ppm, ikk, ipk, gk, ppk)
                time.sleep(3)
                st.session_state.data = dataHandler.load_data()
                st.rerun()
            else:
                st.write("Harap pilih provinsi dan kota terlebih dahulu.")

    # Limit Data
    page_size = 15
    if "page_num" not in st.session_state:
        st.session_state.page_num = 0

    # Filtered data berdasarkan provinsi/kota yang dipilih
    flattened_data = dataHandler.flatten_data(filtered_data)
    total_items = len(flattened_data)
    paginated_data = get_paginated_data(
        flattened_data, st.session_state.page_num, page_size)

    # Menampilkan Data
    st.subheader("Tabel Data Statistik Kemiskinan")

    # Judul Kolom
    col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns(
        10)

    col1.markdown(
        f"<p style='text-align: left; font-weight: bold;'>Provinsi</p>", unsafe_allow_html=True)
    col2.markdown(
        f"<p style='text-align: left; font-weight: bold;'>Kota</p>", unsafe_allow_html=True)
    col3.markdown(
        f"<p style='text-align: center; font-weight: bold;'>Tahun</p>", unsafe_allow_html=True)
    col4.markdown(
        f"<p style='text-align: center; font-weight: bold;'>Persentase Penduduk Miskin</p>", unsafe_allow_html=True)
    col5.markdown(
        f"<p style='text-align: center; font-weight: bold;'>Indeks Kedalaman Kemiskinan</p>", unsafe_allow_html=True)
    col6.markdown(
        f"<p style='text-align: center; font-weight: bold;'>Indeks Keparahan Kemiskinan</p>", unsafe_allow_html=True)
    col7.markdown(
        f"<p style='text-align: center; font-weight: bold;'>Garis Kemiskinan</p>", unsafe_allow_html=True)
    col8.markdown(
        f"<p style='text-align: center; font-weight: bold;'>Pengeluaran per Kapita</p>", unsafe_allow_html=True)
    col9.markdown(
        f"<p style='text-align: center; font-weight: bold;'>Update</p>", unsafe_allow_html=True)
    col10.markdown(
        f"<p style='text-align: center; font-weight: bold;'>Delete</p>", unsafe_allow_html=True)

    # Data Kolom
    for item in paginated_data:
        
        col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns(10)
        
        col1.write(f"<p style='text-align: left;'>{dataHandler.title_case(item['nama_provinsi'])}</p>", unsafe_allow_html=True)
        col2.write(f"<p style='text-align: left;'>{item['nama_kota']}</p>", unsafe_allow_html=True)
        col3.write(f"<p style='text-align: center;'>{item['tahun']}</p>", unsafe_allow_html=True)
        col4.write(f"<p style='text-align: center;'>{item['persentase_penduduk_miskin']}</p>", unsafe_allow_html=True)
        col5.write(f"<p style='text-align: center;'>{item['indeks_kedalaman_kemiskinan']}</p>", unsafe_allow_html=True)
        col6.write(f"<p style='text-align: center;'>{item['indeks_keparahan_kemiskinan']}</p>", unsafe_allow_html=True)
        col7.write(f"<p style='text-align: center;'>{item['garis_kemiskinan']}</p>", unsafe_allow_html=True)
        col8.write(f"<p style='text-align: center;'>{item['pengeluaran_per_kapita']}</p>", unsafe_allow_html=True)

        update_btn = col9.button(
            "Update", key=f"update_{item['_id']}_{item['nama_kota']}")
        delete_btn = col10.button(
            "Delete", key=f"delete_{item['_id']}_{item['nama_kota']}")

        if delete_btn:
            data_id = item['_id']
            nama_kota = item['nama_kota']

            crud.delete_kemiskinan(data_id, nama_kota)
            time.sleep(3)
            st.session_state.data = dataHandler.load_data()
            st.rerun()

        if "active_form_id" not in st.session_state:
            st.session_state.active_form_id = None

        if update_btn:
            st.session_state.active_form_id = {
                "_id": item["_id"], "nama_kota": item["nama_kota"]}

        if st.session_state.active_form_id == {"_id": item["_id"], "nama_kota": item["nama_kota"]}:
            with st.form(f"update_form_{item['_id']}_{item['nama_kota']}"):

                col1, col2 = st.columns(2)
                col3, col4 = st.columns(2)
                col5, col6 = st.columns(2)
                col7, col8 = st.columns(2)

                with col1:
                    prov = st.selectbox("Provinsi", options=[
                                        item['nama_provinsi']], disabled=True)
                with col2:
                    kota = st.selectbox(
                        "Kota", options=[item['nama_kota']], disabled=True)
                with col3:
                    tahun = st.number_input("Tahun", value=item['tahun'])
                with col4:
                    new_ppm = st.number_input("Persentase Penduduk Miskin", value=item['persentase_penduduk_miskin'])
                with col5:
                    new_ikk = st.number_input("Indeks Kedalaman Kemiskinan", value=item['indeks_kedalaman_kemiskinan'])
                with col6:
                    new_ipk = st.number_input("Indeks Keparahan Kemiskinan", value=item['indeks_keparahan_kemiskinan'])
                with col7:
                    new_gk = st.number_input("Garis Kemiskinan", value=item['garis_kemiskinan'])
                with col8:
                    new_ppk = st.number_input("Pengeluaran per Kapita", value=item['pengeluaran_per_kapita'])

                submitted_update = st.form_submit_button("Update Data")

                if submitted_update:
                    updated_data = {
                        "persentase_penduduk_miskin": new_ppm,
                        "indeks_kedalaman_kemiskinan": new_ikk,
                        "indeks_keparahan_kemiskinan": new_ipk,
                        "garis_kemiskinan": new_gk,
                        "pengeluaran_per_kapita": new_ppk
                    }
                    crud.update_kemiskinan(
                        item["_id"], item["nama_kota"], updated_data)
                    time.sleep(3)
                    st.session_state.data = dataHandler.load_data()  # Refresh data setelah delete
                    st.session_state.active_form_id = None
                    st.rerun()

    # Kontrol paginations
    col1, col2, col3 = st.columns([3, 1, 3])
    with col2:

        col_left, col_right = st.columns([1, 1])
        with col_left:
            prev_button = st.button(
                "Previous", key="prev") if st.session_state.page_num > 0 else None
        with col_right:
            next_button = st.button("Next", key="next") if (
                st.session_state.page_num + 1) * page_size <= len(filtered_data) else None

        if prev_button and st.session_state.page_num > 0:
            st.session_state.page_num -= 1
            st.rerun()

        if next_button and (st.session_state.page_num + 1) * page_size <= len(filtered_data):
            st.session_state.page_num += 1
            st.rerun()

elif page == "Bantuan Sosial Pangan":
    st.header("Data Bantuan Sosial Pangan")

    # get data
    filtered_data, provinsi_selected = dataHandler.sidebar_filters(
        data, page)

    filtered_data = [
        item for item in filtered_data if 'bansos' in item and bool(item['bansos'])
    ]

    st.subheader("Tambah Data Statistik Bantuan Sosial Pangan")

    # Inisialisasi session_state untuk provinsi dan kota
    if "selected_provinsi" not in st.session_state:
        st.session_state.selected_provinsi = None

    provinsi_options = ["Pilih Provinsi"] + sorted(list(set(item["nama_provinsi"] for item in data)))
    provinsi = st.selectbox(
        "Pilih Provinsi",
        options=provinsi_options,
        key="selected_provinsi",
    )

    # Form untuk Submit Data
    with st.form("add_data_form"):

        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)
        col5, _ = st.columns(2)

        with col1:
            tahun = st.number_input(
                "Tahun", min_value=2000, max_value=2100, step=1)
        with col2:
            ppm = st.number_input("Rencana Jumlah Keluarga Penerima BANSOS")
        with col3:
            ikk = st.number_input("Realisasi Jumlah Keluarga Penerima BANSOS")
        with col4:
            ipk = st.number_input("Rencana Anggaran BANSOS")
        with col5:
            gk = st.number_input("Realisasi Anggaran BANSOS")

        submitted = st.form_submit_button("Submit")
        if submitted:
            if st.session_state.selected_provinsi:
                crud.add_bansos(tahun, provinsi,
                                ppm, ikk, ipk, gk)
                time.sleep(3)
                st.session_state.data = dataHandler.load_data()
                st.rerun()
            else:
                st.write("Harap pilih provinsi terlebih dahulu.")

    # Limit Data
    page_size = 15 
    if "page_num" not in st.session_state:
        st.session_state.page_num = 0

    # Filtered data berdasarkan provinsi/kota yang dipilih
    flattened_data = dataHandler.flatten_data(
        filtered_data, flatten_style='bansos')
    total_items = len(flattened_data)
    paginated_data = get_paginated_data(
        flattened_data, st.session_state.page_num, page_size)

    # Menampilkan Data
    st.subheader("Tabel Data Bantuan Sosial Pangan")

    # Judul Kolom
    col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(
        8)

    col1.markdown(
        f"<p style='text-align: left; font-weight: bold;'>Provinsi</p>", unsafe_allow_html=True)
    col2.markdown(
        f"<p style='text-align: left; font-weight: bold;'>Tahun</p>", unsafe_allow_html=True)
    col3.markdown(
        f"<p style='text-align: center; font-weight: bold;'>Rencana Jumlah Keluarga Penerima BANSOS</p>", unsafe_allow_html=True)
    col4.markdown(
        f"<p style='text-align: center; font-weight: bold;'>Realisasi Jumlah Keluarga Penerima BANSOS</p>", unsafe_allow_html=True)
    col5.markdown(
        f"<p style='text-align: center; font-weight: bold;'>Rencana Anggaran BANSOS</p>", unsafe_allow_html=True)
    col6.markdown(
        f"<p style='text-align: center; font-weight: bold;'>Realisasi Anggaran BANSOS</p>", unsafe_allow_html=True)
    col7.markdown(
        f"<p style='text-align: center; font-weight: bold;'>Update</p>", unsafe_allow_html=True)
    col8.markdown(
        f"<p style='text-align: center; font-weight: bold;'>Delete</p>", unsafe_allow_html=True)

    # Data Kolom
    for item in paginated_data:

        col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(
            8)
        
        col1.write(
            f"<p style='text-align: left;'>{dataHandler.title_case(item['nama_provinsi'])}</p>", unsafe_allow_html=True)
        col2.write(
            f"<p style='text-align: left;'>{item['tahun']}</p>", unsafe_allow_html=True)
        col3.write(
            f"<p style='text-align: center;'>{item['rencana_keluarga_penerima']}</p>", unsafe_allow_html=True)
        col4.write(
            f"<p style='text-align: center;'>{item['realisasi_keluarga_penerima']}</p>", unsafe_allow_html=True)
        col5.write(
            f"<p style='text-align: center;'>{item['rencana_anggaran']}</p>", unsafe_allow_html=True)
        col6.write(
            f"<p style='text-align: center;'>{item['realisasi_anggaran']}</p>", unsafe_allow_html=True)

        update_btn = col7.button(
            "Update", key=f"update_{item['_id']}")
        delete_btn = col8.button(
            "Delete", key=f"delete_{item['_id']}")

        if delete_btn:
            data_id = item['_id']
            nama_provinsi = item['nama_provinsi']

            crud.delete_bansos(data_id, nama_provinsi)
            time.sleep(3)
            st.session_state.data = dataHandler.load_data()
            st.rerun()

        if "active_form_id" not in st.session_state:
            st.session_state.active_form_id = None

        if update_btn:
            st.session_state.active_form_id = {
                "_id": item["_id"], "nama_provinsi": item["nama_provinsi"]}

        if st.session_state.active_form_id == {"_id": item["_id"], "nama_provinsi": item["nama_provinsi"]}:
            with st.form(f"update_form_{item['_id']}_{item['nama_provinsi']}"):

                col1, col3 = st.columns(2)
                col4, col5 = st.columns(2)
                col6, col7 = st.columns(2)

                with col1:
                    prov = st.selectbox("Provinsi", options=[
                                        item['nama_provinsi']], disabled=True)
                with col3:
                    tahun = st.number_input("Tahun", value=item['tahun'])
                with col4:
                    new_ppm = st.number_input(
                        "Rencana Jumlah Keluarga Penerima BANSOS", value=item['rencana_keluarga_penerima'])
                with col5:
                    new_ikk = st.number_input(
                        "Realisasi Jumlah Keluarga Penerima BANSOS", value=item['realisasi_keluarga_penerima'])
                with col6:
                    new_ipk = st.number_input(
                        "Rencana Anggaran BANSOS", value=item['rencana_anggaran'])
                with col7:
                    new_gk = st.number_input(
                        "Realisasi Anggaran BANSOS", value=item['realisasi_anggaran'])

                submitted_update = st.form_submit_button("Update Data")

                if submitted_update:
                    updated_data = {
                        "rencana_keluarga_penerima": new_ppm,
                        "realisasi_keluarga_penerima": new_ikk,
                        "rencana_anggaran": new_ipk,
                        "realisasi_anggaran": new_gk,
                    }
                    crud.update_bansos(
                        item["_id"], updated_data)
                    time.sleep(3)
                    st.session_state.data = dataHandler.load_data()  # Refresh data setelah delete
                    st.session_state.active_form_id = None
                    st.rerun()

    # Pagination Controls
    col1, col2, col3 = st.columns([3, 1, 3])
    with col2:

        col_left, col_right = st.columns([1, 1])
        with col_left:
            prev_button = st.button(
                "Previous", key="prev") if st.session_state.page_num > 0 else None
        with col_right:
            next_button = st.button("Next", key="next") if (
                st.session_state.page_num + 1) * page_size <= len(filtered_data) else None

        if prev_button and st.session_state.page_num > 0:
            st.session_state.page_num -= 1
            st.rerun()

        if next_button and (st.session_state.page_num + 1) * page_size <= len(filtered_data):
            st.session_state.page_num += 1
            st.rerun()

elif page == "Tingkat Pengangguran":
    st.header("Data Tingkat Pengangguran")

    # get data
    filtered_data, provinsi_selected = dataHandler.sidebar_filters(
        data, page)
    
    filtered_data = [
        item for item in filtered_data if 'tingkat_pengangguran' in item and bool(item['tingkat_pengangguran'])
    ]

    st.subheader("Tambah Data Statistik Tingkat Pengangguran")

    # Inisialisasi session_state untuk provinsi dan kota
    if "selected_provinsi" not in st.session_state:
        st.session_state.selected_provinsi = None

    # Pilihan Provinsi (di luar form untuk mendukung interaktivitas)
    provinsi_options = ["Pilih Provinsi"] + sorted(list(set(item["nama_provinsi"] for item in data)))
    provinsi = st.selectbox(
        "Pilih Provinsi",
        options=provinsi_options,
        key="selected_provinsi",
    )

    # Form untuk Submit Data
    with st.form("add_data_form"):

        col1, col2 = st.columns(2)

        with col1:
            tahun = st.number_input(
                "Tahun", min_value=2000, max_value=2100, step=1)
        with col2:
            ting_peng = st.number_input("Tingkat Pengangguran")

        submitted = st.form_submit_button("Submit")
        if submitted:
            if st.session_state.selected_provinsi:
                crud.add_ting_peng(tahun, provinsi,
                                ting_peng)
                time.sleep(3)
                st.session_state.data = dataHandler.load_data()
                st.rerun()
            else:
                st.write("Harap pilih provinsi terlebih dahulu.")
    
    # Limit Data
    page_size = 15  # Show 15 records per page
    if "page_num" not in st.session_state:
        st.session_state.page_num = 0

    # Filtered data berdasarkan provinsi/kota yang dipilih
    flattened_data = dataHandler.flatten_data(
        filtered_data, flatten_style='tingkat_pengangguran')
    total_items = len(flattened_data)
    paginated_data = get_paginated_data(
        flattened_data, st.session_state.page_num, page_size)
    
    # Menampilkan Data
    st.subheader("Tabel Data Bantuan Sosial Pangan")

    # Judul Kolom
    col1, col2, col3, col4, col5 = st.columns(5)

    col1.markdown(
        f"<p style='text-align: left; font-weight: bold;'>Provinsi</p>", unsafe_allow_html=True)
    col2.markdown(
        f"<p style='text-align: left; font-weight: bold;'>Tahun</p>", unsafe_allow_html=True)
    col3.markdown(
        f"<p style='text-align: center; font-weight: bold;'>Tingkat Pengangguran</p>", unsafe_allow_html=True)
    col4.markdown(
        f"<p style='text-align: center; font-weight: bold;'>Update</p>", unsafe_allow_html=True)
    col5.markdown(
        f"<p style='text-align: center; font-weight: bold;'>Delete</p>", unsafe_allow_html=True)
    
    # Data Kolom
    for item in paginated_data:

        # for kota in item['data_kota']:
        col1, col2, col3, col4, col5 = st.columns(5)
        
        col1.write(
            f"<p style='text-align: left;'>{dataHandler.title_case(item['nama_provinsi'])}</p>", unsafe_allow_html=True)
        col2.write(
            f"<p style='text-align: left;'>{item['tahun']}</p>", unsafe_allow_html=True)
        col3.write(
            f"<p style='text-align: center;'>{item['tingkat_pengangguran']}</p>", unsafe_allow_html=True)
        
        update_btn = col4.button(
            "Update", key=f"update_{item['_id']}")
        delete_btn = col5.button(
            "Delete", key=f"delete_{item['_id']}")
        
        if delete_btn:
            data_id = item['_id']
            nama_provinsi = item['nama_provinsi']

            crud.delete_ting_peng(data_id, nama_provinsi)
            time.sleep(3)
            st.session_state.data = dataHandler.load_data()
            st.rerun()

        if "active_form_id" not in st.session_state:
            st.session_state.active_form_id = None

        if update_btn:
            st.session_state.active_form_id = {
                "_id": item["_id"], "nama_provinsi": item["nama_provinsi"]}
            
        if st.session_state.active_form_id == {"_id": item["_id"], "nama_provinsi": item["nama_provinsi"]}:
            with st.form(f"update_form_{item['_id']}_{item['nama_provinsi']}"):

                col1, col3 = st.columns(2)
                col4, _ = st.columns(2)

                with col1:
                    prov = st.selectbox("Provinsi", options=[
                                        item['nama_provinsi']], disabled=True)
                with col3:
                    tahun = st.number_input("Tahun", value=item['tahun'])
                with col4:
                    new_ting_peng = st.number_input(
                        "Tingkat Pengangguran", value=item['tingkat_pengangguran'])

                submitted_update = st.form_submit_button("Update Data")

                if submitted_update:
                    updated_data = new_ting_peng
                    crud.update_ting_peng(
                        item["_id"], updated_data)
                    time.sleep(3)
                    st.session_state.data = dataHandler.load_data()  # Refresh data setelah delete
                    st.session_state.active_form_id = None
                    st.rerun()
    # Pagination Controls
    col1, col2, col3 = st.columns([3, 1, 3])
    with col2:

        col_left, col_right = st.columns([1, 1])  
        with col_left:
            prev_button = st.button(
                "Previous", key="prev") if st.session_state.page_num > 0 else None
        with col_right:
            next_button = st.button("Next", key="next") if (
                st.session_state.page_num + 1) * page_size <= len(filtered_data) else None

        if prev_button and st.session_state.page_num > 0:
            st.session_state.page_num -= 1
            st.rerun()

        if next_button and (st.session_state.page_num + 1) * page_size <= len(filtered_data):
            st.session_state.page_num += 1
            st.rerun()