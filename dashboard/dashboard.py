import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np
from plot import process_data, plot_pm_variation_combined, plot_weather_pollution_correlation, plot_pollutant_correlation, plot_station_pollutant_avg, display_filtered_dataframe, plot_monthly_pollutant_trends, plot_station_temperature_stats, plot_highest_rainfall_station

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
        with st.container():
            st.subheader("Rata-rata Konsentrasi Polutan per Stasiun")
            pollutants = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
            plot_station_pollutant_avg(combined_df, pollutants, style, palette)
            with st.expander("Penjelasan Konsentrasi Polutan Udara per Stasiun"):
                st.write("""
                            - Aotizhongxin secara konsisten memiliki konsentrasi rata-rata polutan udara (PM2.5, PM10, SO2, NO2, CO) yang lebih tinggi dibandingkan Changping.
                                - Hal ini menunjukkan kualitas udara yang lebih buruk di Aotizhongxin, kemungkinan besar karena aktivitas manusia seperti industri dan transportasi.
                            - Konsentrasi O3 di kedua stasiun relatif sama, menunjukkan pola distribusi yang lebih dipengaruhi oleh proses atmosferik
                        """)

    with tabs[4]:
        with st.container():
            pollutants = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
            plot_monthly_pollutant_trends(
                combined_df, pollutants, style, palette)
            with st.expander("Penjelasan Rata-rata Bulanan Polutan Udara Sepanjang Tahun"):
                st.write("""
                        - Tren Musiman:
                            - CO, PM2.5, PM10, SO2, dan NO2 menunjukkan peningkatan selama musim dingin karena aktivitas manusia yang lebih intensif dan kondisi atmosfer yang menahan polutan.
                            - Ozon (O3) lebih tinggi selama musim panas karena pembentukan fotokimia yang dipengaruhi oleh sinar matahari.

                        - Polusi Puncak:
                            - Musim dingin menunjukkan tingkat polusi udara yang lebih tinggi untuk sebagian besar polutan primer, menandakan kualitas udara yang buruk selama periode ini.
                        """)

    with tabs[5]:
        with st.container():
            plot_station_temperature_stats(combined_df, style, palette)
            with st.expander("Penjelasan Statistik Suhu Stasiun"):
                st.write("""
                            - Suhu Tertinggi: Dicapai di kedua stasiun, yaitu 40°C, selama musim panas.
                            - Suhu Terendah: Dicapai di kedua stasiun, yaitu -10°C, selama musim dingin.
                            - Variasi Musiman: Kedua lokasi menunjukkan perbedaan suhu yang signifikan antara musim panas dan musim dingin, dengan rentang suhu sekitar 50°C.
                        """)

    with tabs[6]:
        with st.container():
            plot_highest_rainfall_station(combined_df, style, palette)
            with st.expander("Penjelasan Curah Hujan Tertinggi Per Stasiun"):
                st.write("""
                            - Curah hujan tertinggi terjadi di stasiun Aotizhongxin, menjadikannya wilayah dengan curah hujan yang lebih intens dibandingkan Changping.
                            - Perbedaan curah hujan antara kedua stasiun dapat disebabkan oleh faktor geografis, topografi, atau pola iklim lokal.
                        """)

    with tabs[7]:
        st.subheader("Kesimpulan")
        st.write("""
                    1. Variasi Kualitas Udara:
                        - PM2.5 dan PM10 menunjukkan pola musiman dengan peningkatan konsentrasi selama musim dingin (Desember-Februari) akibat inversi suhu dan aktivitas manusia.
                        - Aotizhongxin memiliki konsentrasi polusi yang lebih tinggi dibandingkan Changping.
                    
                    2. Korelasi Cuaca dan Polusi:
                        - Suhu (TEMP) memiliki korelasi negatif dengan PM2.5 dan PM10, menunjukkan polusi lebih tinggi pada suhu rendah.
                        - Kecepatan angin (WSPM) berpengaruh signifikan dalam menyebarkan polutan, dengan korelasi negatif terhadap PM2.5 dan PM10.
                        - Tekanan udara (PRES) tidak memiliki hubungan signifikan dengan tingkat polusi.
                    
                    3. Korelasi Antar Polutan:
                        - NO2 dan CO memiliki korelasi kuat positif, menunjukkan sumber emisi yang sama seperti kendaraan bermotor.
                          Ozon (O3) memiliki korelasi negatif dengan NO2 dan CO, menunjukkan proses fotokimia yang berlawanan dengan polutan primer.
                    
                    4. Konsentrasi Polutan per Stasiun:
                        - Aotizhongxin secara konsisten mencatat konsentrasi PM2.5, PM10, SO2, NO2, dan CO yang lebih tinggi dibandingkan Changping, menunjukkan kualitas udara yang lebih buruk di stasiun ini.
                    
                    5. Tren Polusi Sepanjang Tahun:
                        - CO, PM2.5, PM10, SO2, dan NO2 meningkat selama musim dingin akibat aktivitas manusia dan inversi suhu.
                        - Ozon (O3) lebih tinggi selama musim panas, terbentuk melalui reaksi fotokimia di bawah sinar matahari.
                    
                    6. Suhu Ekstrem:
                        - Suhu tertinggi (40°C) dan terendah (-10°C) tercatat di kedua stasiun, menunjukkan variasi musiman yang ekstrem di wilayah ini.
                    
                    7. Curah Hujan Tertinggi:
                        - Aotizhongxin mencatat curah hujan tertinggi (70 mm), lebih tinggi dibandingkan Changping (50 mm), menunjukkan intensitas hujan yang lebih besar di wilayah ini.
                """)


if __name__ == '__main__':
    main()
