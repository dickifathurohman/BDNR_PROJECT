import streamlit as st
import pandas as pd
from connect import *

def add_kemiskinan(tahun, provinsi, kota, ppm, ikk, ipk, gk, ppk):
    
    data_id = f"{provinsi}_{tahun}"

    # Cek apakah data untuk provinsi, kota, dan tahun sudah ada
    existing_data = collection.find_one({
        "_id": data_id,
        "data_kota.nama_kota": kota
    })

    if existing_data:
        st.error(f"Data untuk {kota} pada tahun {tahun} sudah ada!")
    else:
        # Cek apakah data provinsi dan tahun sudah ada
        provinsi_tahun_data = collection.find_one({
            "_id": data_id
        })

        if provinsi_tahun_data:
            # Tambahkan kota baru ke data provinsi dan tahun tersebut
            collection.update_one(
                {"_id": provinsi_tahun_data["_id"]},
                {
                    "$push": {
                        "data_kota": {
                            "nama_kota": kota,
                            "kemiskinan": {
                                "persentase_penduduk_miskin": ppm,
                                "indeks_kedalaman_kemiskinan": ikk,
                                "indeks_keparahan_kemiskinan": ipk,
                                "garis_kemiskinan": gk,
                                "pengeluaran_per_kapita": ppk
                            }
                        }
                    }
                }
            )
        else:
            # Jika data provinsi dan tahun belum ada, tambahkan data baru
            new_data = {
                "_id": data_id,
                "nama_provinsi": provinsi,
                "tahun": tahun,
                "data_kota": [
                    {
                        "nama_kota": kota,
                        "kemiskinan": {
                            "persentase_penduduk_miskin": ppm,
                            "indeks_kedalaman_kemiskinan": ikk,
                            "indeks_keparahan_kemiskinan": ipk,
                            "garis_kemiskinan": gk,
                            "pengeluaran_per_kapita": ppk
                        }
                    }
                ]
            }
            collection.insert_one(new_data)

        st.success("Data berhasil ditambahkan!")

# Fungsi untuk menghapus data kota
def delete_kemiskinan(data_id, kota):
    # Cek apakah data untuk provinsi, kota, dan tahun ada
    existing_data = collection.find_one({
        "_id": data_id,
        "data_kota.nama_kota": kota
    })

    if not existing_data:
        st.error(f"Data tidak ditemukan!")
    else:
        # Hapus data kota dari provinsi dan tahun tersebut
        collection.update_one(
            {
                "_id": data_id
            },
            {
                "$pull": {
                    "data_kota": {
                        "nama_kota": kota
                    }
                }
            }
        )

        # Setelah penghapusan, cek apakah data provinsi masih memiliki data kota
        updated_data = collection.find_one({
            "_id": data_id,
        })

        if not updated_data["data_kota"] and not updated_data.get("bantuan_sosial") and not updated_data.get("pengangguran"):
            collection.delete_one({
                "_id": data_id
            })

        st.success(f"Data berhasil dihapus!")

# Fungsi untuk mengupdate data kemiskinan berdasarkan _id dan nama kota
def update_kemiskinan(_id, nama_kota, updated_values):

    # Query untuk mencocokkan dokumen dengan _id dan nama_kota
    filter_query = {
        "_id": _id,
        "data_kota.nama_kota": nama_kota
    }

    # Perintah update dengan $set
    update_query = {
        "$set": {f"data_kota.$.kemiskinan.{key}": value for key, value in updated_values.items()}
    }

    # Lakukan pembaruan
    result = collection.update_one(filter_query, update_query)

    # Cek hasil pembaruan
    if result.modified_count > 0:
        st.success("Data berhasil diperbarui!")
    else:
        st.error("Gagal memperbarui data. Periksa kembali ID dan Nama Kota.")
    