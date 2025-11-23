'''
=================================================
Milestone 3

Nama  : Yudhistira Pandu D
Batch : FTDS-032-HCK

Program ini dibuat untuk melakukan automatisasi proses data pipeline 
yang meliputi tahap extract, transform, dan load (ETL) dari PostgreSQL 
menuju ElasticSearch menggunakan Apache Airflow.

Adapun dataset yang digunakan merupakan data kendaraan listrik (Electric Vehicle)
yang berisi informasi mengenai spesifikasi teknis, harga, penjualan, dan performa 
mobil listrik dari berbagai produsen. 
Proyek ini bertujuan untuk mendukung analisis performa, tren pasar, serta efisiensi
produk kendaraan listrik yang akan divisualisasikan menggunakan Kibana Dashboard.
=================================================
'''

from airflow import DAG
import pandas as pd
import datetime as dt
from datetime import timedelta
from elasticsearch import Elasticsearch
from elasticsearch import helpers

from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.empty import EmptyOperator
# untuk connect postgre dengan python
import psycopg2 as db


def extract_data():
    """
    Kelas ini bertanggung jawab untuk melakukan proses ekstraksi data
    dari database PostgreSQL. Kelas ini mengatur koneksi ke database,
    menjalankan query, dan menyimpan hasilnya ke dalam file CSV.

    Database yang digunakan: milestone_3
    Tabel yang diambil: table_m3
    """
    conn_string="dbname='milestone_3' " \
    "host='postgres' " \
    "user='airflow' " \
    "password='airflow' " \
    "port = 5432"
    conn=db.connect(conn_string)

    table_m3 = pd.read_sql("select * from table_m3", conn)

    table_m3.to_csv('/opt/airflow/dags/P2M3_yudhistira_data_raw.csv')
    print("-------P2M3_yudhistira_data_raw.csv Saved------")
    

def transform():
    """
    Kelas ini bertanggung jawab untuk melakukan proses transformasi dan pembersihan data
    hasil ekstraksi sebelum diload ke sistem berikutnya (misalnya Elasticsearch).

    Tahapan utama:
    1. Membaca file CSV mentah hasil ekstraksi dari PostgreSQL.
    2. Membersihkan data (menghapus duplikat & nilai kosong).
    3. Menstandarkan format nama kolom menjadi huruf kecil.
    4. Menyimpan hasil akhir ke file CSV baru untuk tahap load.
    """
    table_m3 = pd.read_csv('/opt/airflow/dags/P2M3_yudhistira_data_raw.csv')

    table_m3 = table_m3.drop_duplicates()
    table_m3 = table_m3.dropna()
    table_m3.columns = table_m3.columns.str.lower()
    table_m3.to_csv('/opt/airflow/dags/P2M3_yudhistira_data_clean.csv', index=False)
    print("-------Data Saved------")

def load_data():
    """
    Kelas ini bertanggung jawab untuk melakukan proses Load Data
    dari file CSV hasil transformasi ke dalam Elasticsearch.

    Tahapan utama:
    1. Membaca data hasil transformasi (CSV).
    2. Membuat koneksi ke Elasticsearch.
    3. Mengubah setiap baris data menjadi format dokumen Elasticsearch.
    4. Melakukan bulk insert data ke dalam index tertentu.
    """
    df = pd.read_csv('/opt/airflow/dags/P2M3_yudhistira_data_clean.csv', index_col=0)
    es = Elasticsearch("http://elasticsearch:9200")

    actions = [
    {
        "_index": "milestone_3",
        "_id": i,
        "_source": r.to_dict()    
    }
    for i,r in df.iterrows()
    ]

    response = helpers.bulk(es, actions)
    print(response)

default_args = {
    'owner': 'yudhistira',
    'start_date': dt.datetime(2024, 11, 1, 14) - dt.timedelta(hours = 7),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=5),
}

with DAG('milestone_3',
         default_args=default_args,
         schedule_interval= '10-30/10 9 * * 6',      # '0 * * * *',
         catchup= False) as dag:

    print_starting = BashOperator(task_id='starting',
                               bash_command='echo "I am reading the CSV now....."')
    
    extractData = PythonOperator(task_id='extract_from_postgre',
                             python_callable=extract_data)
    
    transformData = PythonOperator(task_id='data_cleaning',
                                   python_callable=transform)
    
    loadData = PythonOperator(task_id='load_into_database',
                                python_callable=load_data)
    
    print_stop = BashOperator(task_id='stopping',
                               bash_command='echo "I done converting the CSV"')


print_starting >> extractData >> transformData >> loadData >> print_stop


