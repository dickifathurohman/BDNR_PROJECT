import streamlit as st

st.set_page_config(layout="wide", page_title="SDGs Dashboard and CRUD")

# Judul Halaman
st.title("SDG 1: No Poverty di Indonesia")

# Pengantar
st.header("Selamat datang di halaman kami yang didedikasikan untuk SDG 1: No Poverty.")
st.write("""
Kemiskinan merupakan tantangan signifikan yang dihadapi oleh banyak masyarakat di Indonesia. 
SDG 1 bertujuan untuk mengakhiri semua bentuk kemiskinan di mana pun, dan untuk mencapai tujuan ini, 
penting untuk memiliki akses ke data yang akurat dan terkini. Data ini membantu kita memahami 
situasi kemiskinan di berbagai provinsi dan kota di Indonesia.
""")

# Mengapa Data Kemiskinan di Indonesia Penting?
st.subheader("Mengapa Data Kemiskinan di Indonesia Penting?")
st.write("""
Data yang relevan dan terperinci tentang kemiskinan di Indonesia sangat penting untuk:
- **Menganalisis Situasi Lokal:** Memahami tingkat kemiskinan di setiap provinsi dan kota untuk merumuskan kebijakan yang lebih efektif.
- **Mengidentifikasi Wilayah Rentan:** Menemukan daerah-daerah yang paling membutuhkan intervensi dan dukungan.
- **Memantau Perkembangan:** Melihat kemajuan dalam pengurangan kemiskinan dari waktu ke waktu.
""")

# Apa yang Akan Anda Temukan di Dashboard?
st.subheader("Apa yang Akan Anda Temukan di Dashboard?")
st.write("""
Di halaman Dashboard, Anda akan menemukan berbagai visualisasi data yang komprehensif terkait SDG 1: No Poverty di Indonesia, yang mencakup:
1. **Data Kemiskinan:**
   - **Garis Kemiskinan**: Informasi mengenai batas minimum pengeluaran yang diperlukan untuk memenuhi kebutuhan dasar.
   - **Indeks Kedalaman Kemiskinan**: Mengukur seberapa dalam penduduk yang hidup di bawah garis kemiskinan, memberikan gambaran tentang tingkat kesulitan yang dihadapi.
   - **Indeks Keparahan Kemiskinan**: Menunjukkan tingkat ketidaksetaraan di antara penduduk miskin, memberikan wawasan lebih dalam tentang distribusi kemiskinan.
   - **Persentase Penduduk Miskin**: Data yang menunjukkan proporsi penduduk yang hidup di bawah garis kemiskinan di setiap provinsi dan kota.
   - **Pengeluaran per Kapita**: Rincian tentang rata-rata pengeluaran per orang di setiap provinsi dan kota, yang membantu memahami daya beli masyarakat.
2. **Data Bantuan Sosial (BANSOS):**
   - **Rencana Jumlah Keluarga Penerima BANSOS**: Target jumlah keluarga yang direncanakan untuk menerima bantuan sosial di setiap provinsi.
   - **Realisasi Jumlah Keluarga Penerima BANSOS**: Data aktual mengenai jumlah keluarga yang telah menerima bantuan sosial.
   - **Rencana Anggaran BANSOS**: Anggaran yang direncanakan untuk program bantuan sosial di setiap provinsi.
   - **Realisasi Anggaran BANSOS**: Data tentang anggaran yang telah direalisasikan untuk program bantuan sosial.
3. **Tingkat Pengangguran:**
   - **Data Tingkat Pengangguran**: Informasi mengenai persentase pengangguran di setiap provinsi, memberikan gambaran tentang kondisi pasar kerja dan tantangan ekonomi yang dihadapi.
""")

# Ayo Jelajahi Data
st.subheader("Ayo Jelajahi Data!")
st.write("""
Kami mengundang Anda untuk menjelajahi data yang kami sajikan di halaman Dashboard. 
Dengan memahami data ini, kita semua dapat berkontribusi pada upaya pengentasan kemiskinan di Indonesia.
""")

st.write("**Terima kasih telah mengunjungi website kami!** Mari kita bersama-sama memahami dan mengatasi tantangan kemiskinan melalui data yang akurat dan informatif.")