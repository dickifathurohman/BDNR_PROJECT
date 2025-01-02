from connect import *
import pandas as pd
import csv

def read_csv(file_path):
    with open(file_path, mode="r", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def safe_float(value):
    try:
        return float(value.strip()) if value.strip() != '' else None
    except ValueError:
        return None


def safe_int(value):
    try:
        return int(value.strip()) if value.strip() != '' else None
    except ValueError:
        return None


# Membaca dataset
dataset_kemiskinan = read_csv("dataset/dataset_kemiskinan.csv")
dataset_bantuan = read_csv("dataset/dataset_bantuan.csv")
dataset_pengangguran = read_csv("dataset/dataset_pengangguran.csv")

# Mengambil semua kombinasi provinsi dan tahun dari ketiga file
provinsi_tahun = set()

for row in dataset_kemiskinan:
    provinsi_tahun.add((row["Nama Provinsi"].strip(), safe_int(row["Tahun"])))

for row in dataset_bantuan:
    provinsi_tahun.add((row["Nama Provinsi"].strip(), safe_int(row["Tahun"])))

for row in dataset_pengangguran:
    provinsi_tahun.add((row["Nama Provinsi"].strip(), safe_int(row["Tahun"])))

# Inisialisasi data dictionary
data_dict = {
    (provinsi, tahun): {
        "_id": f"{provinsi}_{tahun}",
        "nama_provinsi": provinsi,
        "tahun": tahun,
        "data_kota": [],
        "bansos": {},
        "pengangguran": {}
    }
    for provinsi, tahun in provinsi_tahun
}

# Proses data kemiskinan
for row in dataset_kemiskinan:
    provinsi = row["Nama Provinsi"].strip()
    tahun = safe_int(row["Tahun"])
    kota = row["Nama Kota"].strip()

    key = (provinsi, tahun)

    # Pastikan tidak ada duplikasi provinsi dan tahun
    if key in data_dict:
        data_dict[key]["data_kota"].append({
            "nama_kota": kota,
            "kemiskinan": {
                "garis_kemiskinan": safe_float(row["Garis Kemiskinan"]),
                "indeks_kedalaman_kemiskinan": safe_float(row["Indeks Kedalaman Kemiskinan"]),
                "indeks_keparahan_kemiskinan": safe_float(row["Indeks Keparahan Kemiskinan"]),
                "persentase_penduduk_miskin": safe_float(row["Persentase Penduduk Miskin"]),
                "pengeluaran_per_kapita": safe_float(row["Pengeluaran per Kapita"])
            }
        })

# Proses data bansos
for row in dataset_bantuan:
    provinsi = row["Nama Provinsi"].strip()
    tahun = safe_int(row["Tahun"])

    key = (provinsi, tahun)

    # Pastikan data bansos tidak redundant
    if key in data_dict:
        data_dict[key]["bansos"] = {
            "rencana_keluarga_penerima": safe_int(row["Rencana Jumlah Keluarga Penerima BANSOS"]),
            "realisasi_keluarga_penerima": safe_int(row["Realisasi Jumlah Keluarga Penerima BANSOS"]),
            "rencana_anggaran": safe_float(row["Rencana Anggaran BANSOS"]),
            "realisasi_anggaran": safe_float(row["Realisasi Anggaran BANSOS"])
        }

# Proses data pengangguran
for row in dataset_pengangguran:
    provinsi = row["Nama Provinsi"].strip()
    tahun = safe_int(row["Tahun"])

    key = (provinsi, tahun)

    # Pastikan data pengangguran tidak redundant
    if key in data_dict:
        data_dict[key]["pengangguran"] = {
            "tingkat_pengangguran": safe_float(row["Tingkat Pengangguran"])
        }

# Konversi ke list dokumen
documents = list(data_dict.values())

# Insert ke MongoDB (menghindari duplikasi dokumen yang sama)
for doc in documents:
    collection.replace_one({"_id": doc["_id"]}, doc, upsert=True)

print(f"Berhasil menyinkronkan {len(documents)} dokumen ke MongoDB!")
