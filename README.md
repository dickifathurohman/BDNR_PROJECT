# Dashboard SDGs: No Poverty (Menghapus Kemiskinan)
- 2103842 | Dicki Fathurohman
- 2106515 | Fachri Najm Noer Kartiman
- 2102313 | Muhammad Kamal R

Dashboard SDGs No Poverty adalah sebuah sistem visualisasi data berbasis dashboard yang dirancang untuk mendukung pencapaian Tujuan Pembangunan Berkelanjutan (SDGs) poin pertama: No Poverty (Tanpa Kemiskinan). Proyek ini memanfaatkan teknologi database NoSQL untuk mengelola data terkait kemiskinan di wilayah Jawa Barat.

## Link App
https://kel1-bdnr-dashboardsdgs.streamlit.app

## Teknologi yang digunakan
- **Python**: Digunakan sebagai bahasa pemrograman utama untuk pengolahan data dan pengembangan logika backend.
- **Streamlit**: Framework open-source untuk membangun aplikasi dashboard interaktif dengan antarmuka yang ramah pengguna.
- **MongoDB**: Database NoSQL untuk menyimpan data kemiskinan dengan struktur fleksibel, memungkinkan pengelolaan data yang besar dan kompleks.
- **Altair**: Pustaka Python untuk membuat visualisasi data statistik berbasis deklaratif. Altair memungkinkan kita membuat grafik yang bersih, estetik, dan interaktif dengan sintaks yang sederhana.
- **Plotly**: Pustaka visualisasi data interaktif yang mendukung berbagai jenis grafik, seperti map, scatter plot, dan diagram 3D
- **Pandas**: Pustaka Python yang sangat populer untuk manipulasi dan analisis data. Pandas menyediakan struktur data seperti DataFrame yang memudahkan pengolahan, transformasi, dan eksplorasi dataset besar.

## Instruksi Run di Lokal
1. Install mongodb
2. Install requirements
3. Buat database dan koleksi dengan menjalankan file insert_data.py (python insert_data.py)
4. Jalankan streamlit pada file Home.py (streamlit run Home.py)
