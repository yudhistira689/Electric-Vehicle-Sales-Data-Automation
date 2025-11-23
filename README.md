# Judul Project
Electric Vehicle Sales Data Automation — Milestone 3
## Repository Outline
1. Description.md — Penjelasan umum tentang project dan komponennya.
2. P2M3_yudhistira_conceptual.txt - Berisi jawaban dari soal Conceptual dari rubics.
3. P2M3_yudhistira_DAG_graph.jpg - Gambar alur DAG yang sudah berjalan dengan baik.
4. P2M3_yudhistira_DAG.py — Script utama DAG Airflow untuk proses ETL otomatis,serta terdapat class dan function untuk proses Extract, Transform, dan Load.
5. P2M3_yudhistira_data_raw.csv — Data set awal untuk dimasukan ke Postgre SQL.
6. P2M3_yudhistira_data_clean.csv — Data hasil transformasi sebelum dimuat ke Elasticsearch.
7. P2M3_yudhistira_ddl.txt - Berisi url dataset, syntax DDL dan DML
8. P2M3_yudhistira_GX.ipynb — Notebook untuk eksplorasi data (EDA) awal.
9. Folder images — Folder berisi gambar/visualisasi dari dashboard Kibana.


## Problem Background
Seiring meningkatnya penggunaan kendaraan listrik (Electric Vehicle/EV) di berbagai negara, kebutuhan untuk menganalisis data penjualan, efisiensi baterai, dan tren harga menjadi sangat penting bagi perusahaan otomotif.
Namun, proses analisis data sering kali memakan waktu karena data tersebar di berbagai sumber dan tidak terotomatisasi.

Proyek ini dibuat untuk mengotomatisasi proses Extract, Transform, dan Load (ETL) dari database PostgreSQL menuju Elasticsearch menggunakan Apache Airflow, sehingga data dapat langsung divisualisasikan melalui Kibana Dashboard.

## Project Output
Output akhir dari proyek ini adalah:
- Pipeline ETL otomatis menggunakan Airflow (dari PostgreSQL → transformasi data → Elasticsearch).
- Dashboard interaktif di Kibana yang menampilkan analisis penjualan, tren harga, dan efisiensi kendaraan listrik.
- Dataset bersih (clean data) yang siap digunakan untuk analisis lebih lanjut.

## Data
Dataset yang digunakan merupakan data penjualan mobil listrik.
Berikut ringkasan karakteristiknya:
Informasi           Deskripsi
Sumber data	        Dataset internal (CSV lokal yang diunggah ke PostgreSQL).
Jumlah baris	    1,845
Jumlah kolom	    17
Kolom utama	        manufacturer, model, year, battery_capacity_kwh, range_km, price_usd, safety_rating, 
                    units_sold_2024
Missing value	    Tidak ada (telah dibersihkan saat tahap transformasi).
Duplicate data	    Sudah dihapus dalam tahap transformasi.


## Method
Metodologi yang digunakan adalah ETL Automation Pipeline, terdiri dari tiga tahapan utama:
1. Extract
    - Mengambil data dari database PostgreSQL (milestone_3).
    - Menyimpan data mentah ke file CSV sementara.

2. Transform
    - Menghapus data duplikat dan nilai kosong.
    - Menstandarkan format kolom (mengubah nama kolom menjadi lowercase).
    - Menyimpan hasil ke file P2M3_yudhistira_data_clean.csv.

3. Load
    - Memasukkan data bersih ke dalam Elasticsearch Index (milestone_3) menggunakan helpers.bulk().
    - Data siap untuk divisualisasikan melalui Kibana.

## Stacks
Berikut teknologi yang digunakan dalam proyek ini:
Kategori	                        Tools / Library
Bahasa Pemrograman	                Python
Orkestrasi Workflow	                Apache Airflow
Database	                        PostgreSQL
Search Engine & Dashboard	        Elasticsearch, Kibana
Library Python	                    pandas, psycopg2, elasticsearch, elasticsearch.helpers
Lingkungan Deployment	            Docker

## Reference
https://www.elastic.co/guide/en/kibana/current/dashboard.html
https://www.kaggle.com/datasets/pratyushpuri/ev-electrical-vehicles-dataset-3k-records-2025

---

## Kesimpulan 
Pipeline ETL ini membantu perusahaan otomotif melakukan integrasi data dan analisis penjualan kendaraan listrik secara otomatis.
Dengan otomatisasi ini, tim R&D, Marketing, dan Sales & Distribution dapat mengakses insight terbaru langsung dari dashboard tanpa perlu melakukan proses manual berulang.