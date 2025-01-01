# BDNR_PROJECT
 
## Struktur Data
{
  "_id": f"{provinsi}_{tahun}",
  "nama_provinsi": provinsi,
  "tahun": tahun,
  "data_kota": [{
     "nama_kota": string,
     "garis_kemiskinan": float,
     "indeks_keparahan_kemiskinan": float,
     "indeks_kedalaman_kemiskinan": float,
     "persentase_penduduk_miskin": float,
     "pengeluaran_per_kapita": float
   }],
  "bansos": {
     "rencana_keluarga_penerima": int,
     "realisasi_keluarga_penerima": int,
     "rencana_anggaran": float,
     "realisasi_anggaran": float
  },
  "pengangguran": {
     "tingkat_pengangguran": float
  }
 }
