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


def add_bansos(tahun, provinsi, ppm, ikk, ipk, gk):

    data_id = f"{provinsi}_{tahun}"

    # Cek apakah data bansos sudah ada
    existing_data = collection.find_one({
        "_id": data_id,
        "bansos.rencana_keluarga_penerima": {"$exists": True}
    })

    if existing_data:
        st.error(f"Data untuk {provinsi} pada tahun {tahun} sudah ada!")
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
                    "$set": {
                        "bansos.rencana_keluarga_penerima": ppm,
                        "bansos.realisasi_keluarga_penerima": ikk,
                        "bansos.rencana_anggaran": ipk,
                        "bansos.realisasi_anggaran": gk
                    }
                }
            )
        else:
            # Jika data provinsi dan tahun belum ada, tambahkan data baru
            new_data = {
                "_id": data_id,
                "nama_provinsi": provinsi,
                "tahun": tahun,
                "bansos": {
                    "rencana_keluarga_penerima": ppm,
                    'realisasi_keluarga_penerima': ikk,
                    'rencana_anggaran': ipk,
                    'realisasi_anggaran': gk
                }
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

        if not updated_data["data_kota"] and not updated_data.get("bansos") and not updated_data.get("pengangguran"):
            collection.delete_one({
                "_id": data_id
            })

        st.success(f"Data berhasil dihapus!")


def delete_bansos(data_id, provinsi):
    # Cek apakah data untuk provinsi, kota, dan tahun ada
    existing_data = collection.find_one({
        "_id": data_id,
        "nama_provinsi": provinsi
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
                "$set": {
                    "bansos": {}  # Mengubah 'bansos' menjadi objek kosong
                }
            }
        )

        # Setelah penghapusan, cek apakah data provinsi masih memiliki data kota
        updated_data = collection.find_one({
            "_id": data_id,
        })

        if not updated_data["data_kota"] and not updated_data.get("bansos") and not updated_data.get("pengangguran"):
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


def update_bansos(_id, updated_values):

    # Query untuk mencocokkan dokumen dengan _id
    filter_query = {
        "_id": _id,
    }

    # Perintah update dengan $set
    update_query = {
        "$set": {f"bansos.{key}": value for key, value in updated_values.items()}
    }

    # Lakukan pembaruan
    result = collection.update_one(filter_query, update_query)

    # Cek hasil pembaruan
    if result.modified_count > 0:
        st.success("Data berhasil diperbarui!")
    else:
        st.error("Gagal memperbarui data. Periksa kembali ID dan Nama Kota.")
