import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np
from plot import process_data, plot_pm_variation_combined, plot_weather_pollution_correlation, plot_pollutant_correlation, plot_station_pollutant_avg, display_filtered_dataframe

# Mengatur konfigurasi halaman sebelum elemen lain
st.set_page_config(
    page_title="Dashboard Kualitas Udara",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Mengatur gaya seaborn default
sns.set(style='darkgrid')


def main():
    """
    Fungsi utama untuk menjalankan aplikasi Streamlit.
    """
    st.title("Dashboard Kualitas Udara")

    # Sidebar untuk pengaturan plot
    st.sidebar.header("Pengaturan Plot")

    # Pilih gaya seaborn
    style = st.sidebar.selectbox(
        'Pilih Gaya Seaborn',
        ('darkgrid', 'whitegrid', 'dark', 'white', 'ticks')
    )

    # Pilih context seaborn
    context = st.sidebar.selectbox(
        'Pilih Context Seaborn',
        ('paper', 'notebook', 'talk', 'poster')
    )
    sns.set_context(context)

    # Pilih palet warna seaborn
    palette = st.sidebar.selectbox(
        'Pilih Palet Warna Seaborn',
        ('deep', 'muted', 'bright', 'pastel', 'dark', 'colorblind')
    )

    # Path ke file CSV
    file_path = 'dashboard/combined_data.csv'

    # Memuat dan memproses data
    combined_df = process_data(file_path)

    st.subheader("Overview")
    st.write("This dashboard contains a bunch of analysis result of an air quality dataset provided by Dicoding Academy. The dataset itself includes information about various air pollutants such as SO2, NO2, CO, O3, as well as temperature, pressure, rain, wind direction, and wind speed.")

    # Menampilkan DataFrame yang telah diproses
    st.subheader("Data Kualitas Udara")
    st.write(
        "Berikut adalah data yang saya gunakan, data tersebut berasal dari [GitHub Repository](https://github.com/marceloreis/HTI/tree/master).")
    display_filtered_dataframe(combined_df)

    # Menambahkan Pertanyaan Bisnis
    st.subheader('Pertanyaan Bisnis')
    st.write("1. Bagaimana kualitas udara (khususnya tingkat PM2.5 dan PM10) bervariasi pada waktu yang berbeda sepanjang tahun di Changping dan Aotizhongxin?")
    st.write("2. Apa korelasi antara kondisi cuaca (misalnya, suhu, kecepatan angin, dan tekanan) dan tingkat polusi di wilayah ini?")
    st.write(
        "3. Apakah ada korelasi antara berbagai polutan udara (SO2, NO2, CO, O3)?")
    st.write("4. Bagaimana konsentrasi polutan udara di berbagai lokasi stasiun?")
    st.write(
        "5. Apakah ada tren atau pola yang terlihat pada tingkat polutan sepanjang tahun?")
    st.write("6. Pada stasiun mana suhu mencapai derajat terendah dan tertingginya?")
    st.write("7. Pada stasiun mana curah hujan mencapai volume tertingginya?")

    # Membuat Tabs untuk Memisahkan Plot
    tabs = st.tabs(["Pertanyaan Bisnis No.1",
                   "Pertanyaan Bisnis No.2", "Pertanyaan Bisnis No.3", "Pertanyaan Bisnis No.4", "Pertanyaan Bisnis No.5", "Pertanyaan Bisnis No.6", "Pertanyaan Bisnis No.7", "Kesimpulan"])

    # Tab untuk Pertanyaan Bisnis No.1
    with tabs[0]:
        # Menampilkan grafik PM2.5 dengan container dan expander
        with st.container():
            st.subheader("Tren Rata-rata Bulanan PM2.5 dan PM10")
            plot_pm_variation_combined(combined_df, style, palette)
            with st.expander("Penjelasan Tren Rata-rata Bulanan PM2.5 dan PM10"):
                st.write("""
                    - Musim Dingin (Desember - Februari): Baik PM2.5 maupun PM10 meningkat signifikan, menunjukkan kualitas udara yang memburuk. Hal ini dapat meningkatkan risiko kesehatan, terutama bagi individu yang rentan terhadap penyakit pernapasan.
                    - Musim Panas (Juni - Agustus): Kualitas udara relatif lebih baik dengan tingkat PM2.5 dan PM10 yang lebih rendah, meskipun Aotizhongxin tetap menunjukkan polusi yang lebih tinggi dibandingkan Changping.
                        """)

    # Tab untuk Pertanyaan Bisnis No.2
    with tabs[1]:
        # Menampilkan grafik Korelasi antara Cuaca dan Polusi dengan container dan expander
        with st.container():
            st.subheader(
                "Korelasi Kondisi Cuaca dan Tingkat Polusi")
            # Menambahkan label bahwa ini adalah jawaban untuk pertanyaan bisnis No.2
            # st.markdown("**Menjawab Pertanyaan Bisnis No.2**")
            plot_weather_pollution_correlation(combined_df, style, palette)
            with st.expander("Penjelasan Correlation Heatmap"):
                st.write("""
                        - Aotizhongxin cenderung memiliki konsentrasi PM2.5 dan PM10 yang lebih tinggi dibandingkan Changping, terlihat dari distribusi yang lebih lebar pada scatter plot.
                        - Suhu (TEMP) dan kecepatan angin (WSPM) memiliki dampak signifikan terhadap tingkat polusi, di mana suhu rendah dan kecepatan angin rendah meningkatkan konsentrasi polusi.
                        - Tekanan udara (PRES) tidak menunjukkan hubungan yang signifikan dengan polusi
                        """)

    # Tab untuk Pertanyaan Bisnis No.3
    with tabs[2]:
        with st.container():
            st.subheader("Korelasi Antar Polutan Udara")
            plot_pollutant_correlation(combined_df, style, palette)
            with st.expander("Penjelasan Korelasi Antar Polutan"):
                st.write("""
                        - Polutan Primer:
                            - NO2 dan CO menunjukkan hubungan yang kuat, menunjukkan bahwa keduanya berasal dari sumber utama yang sama, seperti emisi kendaraan.
                            - SO2 memiliki korelasi moderat dengan NO2 dan CO, mencerminkan kontribusi dari pembakaran bahan bakar fosil.

                        - Polutan Sekunder (O3):
                            - Ozon (O3) memiliki hubungan negatif dengan NO2 dan CO, yang dapat dijelaskan oleh reaksi fotokimia di atmosfer. Ozon terbentuk ketika VOCs (volatile organic compounds) dan NOx bereaksi di bawah sinar matahari, sehingga konsentrasi tinggi NO2 dapat mengurangi ozon di lokasi tertentu.
                        """)

    # Tab untuk Pertanyaan Bisnis No.4
    with tabs[3]:
        st.subheader("Rata-rata Konsentrasi Polutan per Stasiun")
        pollutants = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
        plot_station_pollutant_avg(combined_df, pollutants, style, palette)
        with st.expander("Penjelasan Konsentrasi Polutan Udara per Stasiun"):
            st.write("""
                        - Aotizhongxin secara konsisten memiliki konsentrasi rata-rata polutan udara (PM2.5, PM10, SO2, NO2, CO) yang lebih tinggi dibandingkan Changping.
                            - Hal ini menunjukkan kualitas udara yang lebih buruk di Aotizhongxin, kemungkinan besar karena aktivitas manusia seperti industri dan transportasi.
                        - Konsentrasi O3 di kedua stasiun relatif sama, menunjukkan pola distribusi yang lebih dipengaruhi oleh proses atmosferik
                    """)


if __name__ == '__main__':
    main()
