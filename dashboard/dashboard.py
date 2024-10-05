# dashboard.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Mengatur tampilan visualisasi
sns.set_style('whitegrid')
# plt.style.use('whitegrid')

# Memuat dataset
day_df = pd.read_csv('data/day.csv')
hour_df = pd.read_csv('data/hour.csv')

# Konversi kolom tanggal
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# Pengaturan halaman
st.set_page_config(page_title='Dashboard Bike Sharing', layout='wide')

# Judul dan Pengantar
st.title('Dashboard Analisis Data Layanan Bike Sharing')
st.markdown("""
Dashboard ini menyajikan analisis data layanan bike sharing, mengeksplorasi faktor-faktor yang memengaruhi permintaan penyewaan sepeda, dan memberikan wawasan bisnis.
""")

# Sidebar untuk navigasi
st.sidebar.title('Navigasi')
options = st.sidebar.radio('Pilih Analisis:', ['Data Overview', 'Pengaruh Suhu terhadap Permintaan', 'Pola Penggunaan per Jam', 'Tren Musiman', 'Perbandingan Pengguna'])

# Data Overview
if options == 'Data Overview':
    st.header('Data Overview')
    st.subheader('Dataset Harian')
    st.write(day_df.head())
    st.subheader('Dataset Per Jam')
    st.write(hour_df.head())

    st.markdown('---')
    st.subheader('Statistik Deskriptif')
    st.write(day_df.describe())

# Pengaruh Suhu terhadap Permintaan (Pertanyaan 1)
elif options == 'Pengaruh Suhu terhadap Permintaan':
    st.header('Pengaruh Suhu terhadap Permintaan Penyewaan Sepeda')

    # Menggunakan Clustering dengan Binning dengan kategori suhu (Rendah, Sedang, Tinggi)
    day_df['temp_category'] = pd.cut(day_df['temp'],
                                     bins=[day_df['temp'].min(), 0.33, 0.66, day_df['temp'].max()],
                                     labels=['Rendah', 'Sedang', 'Tinggi'])

    # Melihat distribusi kategori suhu
    temp_counts = day_df['temp_category'].value_counts().sort_index()
    st.subheader('Distribusi Kategori Suhu')
    st.bar_chart(temp_counts)

    # Box plot jumlah penyewaan berdasarkan kategori suhu
    fig, ax = plt.subplots()
    sns.boxplot(x='temp_category', y='cnt', data=day_df, order=['Rendah', 'Sedang', 'Tinggi'], ax=ax)
    ax.set_title('Jumlah Penyewaan Berdasarkan Kategori Suhu')
    ax.set_xlabel('Kategori Suhu')
    ax.set_ylabel('Jumlah Penyewaan')
    st.pyplot(fig)

# Pola Penggunaan per Jam (Pertanyaan 2)
elif options == 'Pola Penggunaan per Jam':
    st.header('Pola Penggunaan per Jam dalam Sehari Berdasarkan Tipe Hari')

    # Menandai hari sebagai 'Hari Kerja' atau 'Akhir Pekan/Hari Libur'
    hour_df['day_type'] = hour_df['workingday'].apply(lambda x: 'Hari Kerja' if x == 1 else 'Akhir Pekan/Hari Libur')

    # Rata-rata penyewaan per jam berdasarkan tipe hari
    avg_hourly_usage = hour_df.groupby(['hr', 'day_type'])['cnt'].mean().reset_index()

    # Visualisasi rata-rata penyewaan per jam
    fig, ax = plt.subplots()
    sns.lineplot(x='hr', y='cnt', hue='day_type', data=avg_hourly_usage, ax=ax)
    ax.set_title('Rata-rata Penyewaan per Jam Berdasarkan Tipe Hari')
    ax.set_xlabel('Jam')
    ax.set_ylabel('Rata-rata Jumlah Penyewaan')
    ax.set_xticks(range(0,24))
    ax.legend(title='Tipe Hari')
    st.pyplot(fig)

# Tren Musiman
elif options == 'Tren Musiman':
    st.header('Tren Musiman dalam Penggunaan Layanan')

    # Menambahkan nama bulan
    day_df['month_name'] = day_df['dteday'].dt.strftime('%b')
    month_order = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

    # Rata-rata penyewaan per bulan
    monthly_usage = day_df.groupby('month_name')['cnt'].mean().reindex(month_order).reset_index()

    # Visualisasi
    fig, ax = plt.subplots()
    sns.barplot(x='month_name', y='cnt', data=monthly_usage, ax=ax)
    ax.set_title('Rata-rata Penyewaan per Bulan')
    ax.set_xlabel('Bulan')
    ax.set_ylabel('Rata-rata Jumlah Penyewaan')
    st.pyplot(fig)

# Perbandingan Pengguna
elif options == 'Perbandingan Pengguna':
    st.header('Perbandingan Pengguna Kasual dan Terdaftar')

    # Total penyewaan per tipe pengguna
    user_usage = day_df[['casual', 'registered']].sum().reset_index()
    user_usage.columns = ['User Type', 'Total Usage']

    # Visualisasi
    fig, ax = plt.subplots()
    sns.barplot(x='User Type', y='Total Usage', data=user_usage, ax=ax)
    ax.set_title('Total Penyewaan Berdasarkan Tipe Pengguna')
    ax.set_xlabel('Tipe Pengguna')
    ax.set_ylabel('Total Penyewaan')
    st.pyplot(fig)

    # Persentase penggunaan
    total_usage = user_usage['Total Usage'].sum()
    user_usage['Percentage'] = user_usage['Total Usage'] / total_usage * 100

    # Pie Chart
    fig2, ax2 = plt.subplots()
    ax2.pie(user_usage['Total Usage'], labels=user_usage['User Type'], autopct='%1.1f%%', colors=['lightblue', 'orange'])
    ax2.set_title('Persentase Penyewaan Berdasarkan Tipe Pengguna')
    st.pyplot(fig2)

# Rekomendasi
st.sidebar.markdown('---')
if st.sidebar.button('Tampilkan Tindakan Lanjutan'):
    st.header('Tindakan Lanjutan')
    st.markdown("""
    ** Tindakan lanjutan berdasarkan hasil analisis data**

    1. Memaksimalkan ketersediaan sepeda pada jam-jam puncak dan musim dengan penggunaan tinggi.
    2. Meningkatkan promosi pada dan inovasi pada musim dingin untuk meningkatkan penggunaan.
    3. Membuat semacam program untuk menarik pengguna casual menjadi pelanggan (registered)
    """)
