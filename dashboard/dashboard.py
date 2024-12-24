import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np

# Mengatur konfigurasi halaman sebelum elemen lain
st.set_page_config(
    page_title="Dashboard Kualitas Udara",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Mengatur gaya seaborn default
sns.set(style='darkgrid')


@st.cache_data
def process_data(file_path):
    """
    Membaca dan memproses data dari file CSV.

    Parameters:
    - file_path (str): Path ke file CSV.

    Returns:
    - pd.DataFrame: DataFrame yang telah diproses.
    """
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        st.error(f"File '{file_path}' tidak ditemukan. Pastikan path benar.")
        st.stop()
    except pd.errors.EmptyDataError:
        st.error("File CSV kosong.")
        st.stop()
    except Exception as e:
        st.error(f"Terjadi kesalahan saat membaca file CSV: {e}")
        st.stop()

    # Membuat kolom 'date' dari 'year', 'month', 'day', 'hour' jika tersedia
    if {'year', 'month', 'day', 'hour'}.issubset(df.columns):
        df['date'] = pd.to_datetime(
            df[['year', 'month', 'day', 'hour']], errors='coerce')
    else:
        st.error(
            "Kolom 'year', 'month', 'day', atau 'hour' tidak ditemukan dalam data.")
        st.stop()

    # Mengonversi kolom 'date' ke tipe datetime
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        missing_dates = df['date'].isna().sum()
        if missing_dates > 0:
            df = df.dropna(subset=['date'])
        df = df.sort_values(by='date').reset_index(drop=True)
    else:
        st.error("Kolom 'date' tidak ditemukan dalam data.")
        st.stop()

    # Menambahkan kolom 'month' dan 'season'
    df['month'] = df['date'].dt.month

    def get_season(month):
        if month in [12, 1, 2]:
            return 'Winter'
        elif month in [3, 4, 5]:
            return 'Spring'
        elif month in [6, 7, 8]:
            return 'Summer'
        else:
            return 'Fall'

    df['season'] = df['month'].apply(get_season)

    return df


def plot_pm25_over_time(df, style, palette):
    """
    Membuat plot PM2.5 variasi waktu untuk seluruh data.

    Parameters:
    - df (pd.DataFrame): DataFrame yang telah diproses.
    - style (str): Gaya seaborn yang dipilih.
    - palette (str): Palet warna seaborn yang dipilih.
    """
    if 'PM2.5' not in df.columns or 'date' not in df.columns or 'station' not in df.columns:
        st.error("Kolom 'PM2.5', 'date', atau 'station' tidak ditemukan dalam data.")
        return

    plt.figure(figsize=(12, 6))
    sns.set_style(style)
    sns.set_palette(palette)
    sns.lineplot(data=df, x='date', y='PM2.5', hue='station', marker='o')
    plt.title('PM2.5 Variation over Time (Aotizhongxin and Changping)')
    plt.xlabel('Date')
    plt.ylabel('PM2.5 Concentration')
    plt.legend(title='Station')
    st.pyplot(plt.gcf())
    plt.clf()


def plot_pm10_over_time(df, style, palette):
    """
    Membuat plot PM10 variasi waktu untuk seluruh data.

    Parameters:
    - df (pd.DataFrame): DataFrame yang telah diproses.
    - style (str): Gaya seaborn yang dipilih.
    - palette (str): Palet warna seaborn yang dipilih.
    """
    if 'PM10' not in df.columns or 'date' not in df.columns or 'station' not in df.columns:
        st.error("Kolom 'PM10', 'date', atau 'station' tidak ditemukan dalam data.")
        return

    plt.figure(figsize=(12, 6))
    sns.set_style(style)
    sns.set_palette(palette)
    sns.lineplot(data=df, x='date', y='PM10', hue='station', marker='o')
    plt.title('PM10 Variation over Time (Aotizhongxin and Changping)')
    plt.xlabel('Date')
    plt.ylabel('PM10 Concentration')
    plt.legend(title='Station')
    st.pyplot(plt.gcf())
    plt.clf()


def plot_average_monthly_pm25(df, style, palette):
    """
    Membuat plot rata-rata bulanan PM2.5 per stasiun.

    Parameters:
    - df (pd.DataFrame): DataFrame yang telah diproses.
    - style (str): Gaya seaborn yang dipilih.
    - palette (str): Palet warna seaborn yang dipilih.
    """
    if 'PM2.5' not in df.columns or 'month' not in df.columns or 'station' not in df.columns:
        st.error("Kolom 'PM2.5', 'month', atau 'station' tidak ditemukan dalam data.")
        return

    monthly_pollution_station = df.groupby(['station', 'month'])[
        ['PM2.5']].mean().reset_index()

    plt.figure(figsize=(12, 6))
    sns.set_style(style)
    sns.set_palette(palette)
    sns.lineplot(data=monthly_pollution_station, x='month',
                 y='PM2.5', hue='station', marker='o')
    plt.title('Average Monthly PM2.5 Levels by Station')
    plt.xlabel('Month')
    plt.ylabel('PM2.5 Concentration')
    plt.xticks(np.arange(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    plt.legend(title='Station')
    st.pyplot(plt.gcf())
    plt.clf()


def plot_average_monthly_pm10(df, style, palette):
    """
    Membuat plot rata-rata bulanan PM10 per stasiun.

    Parameters:
    - df (pd.DataFrame): DataFrame yang telah diproses.
    - style (str): Gaya seaborn yang dipilih.
    - palette (str): Palet warna seaborn yang dipilih.
    """
    if 'PM10' not in df.columns or 'month' not in df.columns or 'station' not in df.columns:
        st.error("Kolom 'PM10', 'month', atau 'station' tidak ditemukan dalam data.")
        return

    monthly_pollution_station = df.groupby(['station', 'month'])[
        ['PM10']].mean().reset_index()

    plt.figure(figsize=(12, 6))
    sns.set_style(style)
    sns.set_palette(palette)
    sns.lineplot(data=monthly_pollution_station, x='month',
                 y='PM10', hue='station', marker='o')
    plt.title('Average Monthly PM10 Levels by Station')
    plt.xlabel('Month')
    plt.ylabel('PM10 Concentration')
    plt.xticks(np.arange(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
    plt.legend(title='Station')
    st.pyplot(plt.gcf())
    plt.clf()


def plot_average_seasonal_pm25(df, style, palette):
    """
    Membuat plot rata-rata musiman PM2.5 per stasiun.

    Parameters:
    - df (pd.DataFrame): DataFrame yang telah diproses.
    - style (str): Gaya seaborn yang dipilih.
    - palette (str): Palet warna seaborn yang dipilih.
    """
    if 'PM2.5' not in df.columns or 'season' not in df.columns or 'station' not in df.columns:
        st.error(
            "Kolom 'PM2.5', 'season', atau 'station' tidak ditemukan dalam data.")
        return

    seasonal_pollution_station = df.groupby(['station', 'season'])[
        ['PM2.5']].mean().reset_index()

    plt.figure(figsize=(10, 6))
    sns.set_style(style)
    sns.set_palette(palette)
    sns.barplot(x='season', y='PM2.5', hue='station',
                data=seasonal_pollution_station, palette='Set2')
    plt.title('Average Seasonal PM2.5 Levels by Station')
    plt.xlabel('Season')
    plt.ylabel('PM2.5 Concentration')
    plt.legend(title='Station')
    st.pyplot(plt.gcf())
    plt.clf()


def plot_average_seasonal_pm10(df, style, palette):
    """
    Membuat plot rata-rata musiman PM10 per stasiun.

    Parameters:
    - df (pd.DataFrame): DataFrame yang telah diproses.
    - style (str): Gaya seaborn yang dipilih.
    - palette (str): Palet warna seaborn yang dipilih.
    """
    if 'PM10' not in df.columns or 'season' not in df.columns or 'station' not in df.columns:
        st.error("Kolom 'PM10', 'season', atau 'station' tidak ditemukan dalam data.")
        return

    seasonal_pollution_station = df.groupby(['station', 'season'])[
        ['PM10']].mean().reset_index()

    plt.figure(figsize=(10, 6))
    sns.set_style(style)
    sns.set_palette(palette)
    sns.barplot(x='season', y='PM10', hue='station',
                data=seasonal_pollution_station, palette='Set1')
    plt.title('Average Seasonal PM10 Levels by Station')
    plt.xlabel('Season')
    plt.ylabel('PM10 Concentration')
    plt.legend(title='Station')
    st.pyplot(plt.gcf())
    plt.clf()


def plot_correlation_heatmap(df, style, palette):
    """
    Membuat heatmap korelasi antara kondisi cuaca dan tingkat polusi.

    Parameters:
    - df (pd.DataFrame): DataFrame yang telah diproses.
    - style (str): Gaya seaborn yang dipilih.
    - palette (str): Palet warna seaborn yang dipilih.
    """
    corr_columns = ['PM2.5', 'PM10', 'TEMP', 'WSPM', 'PRES']
    if not set(corr_columns).issubset(df.columns):
        st.error(f"Kolom-kolom {corr_columns} tidak ditemukan dalam data.")
        return

    corr_matrix = df[corr_columns].corr()

    plt.figure(figsize=(8, 6))
    sns.set_style(style)
    sns.set_palette(palette)
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', vmin=-1, vmax=1)
    plt.title('Correlation between Weather Conditions and Pollution Levels')
    st.pyplot(plt.gcf())
    plt.clf()


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
    file_path = 'https://raw.githubusercontent.com/paizramadhan/analisis-data-dicoding/main/dashboard/combined_data.csv'

    # Memuat dan memproses data
    combined_df = process_data(file_path)

    # Menampilkan DataFrame yang telah diproses
    st.subheader("Data Kualitas Udara")
    st.write(
        "Berikut adalah data yang saya gunakan, data tersebut berasal dari [GitHub Repository](https://github.com/marceloreis/HTI/tree/master).")
    st.dataframe(combined_df)

    # Menambahkan Pertanyaan Bisnis
    st.subheader('Pertanyaan Bisnis')
    st.write("1. Bagaimana kualitas udara (khususnya tingkat PM2.5 dan PM10) bervariasi pada waktu yang berbeda sepanjang tahun di Changping dan Aotizhongxin?")
    st.write("2. Apa korelasi antara kondisi cuaca (misalnya, suhu, kecepatan angin, dan tekanan) dan tingkat polusi di wilayah ini?")

    # Membuat Tabs untuk Memisahkan Plot
    tabs = st.tabs(["Pertanyaan Bisnis No.1",
                   "Pertanyaan Bisnis No.2", "Kesimpulan"])

    # Tab untuk Pertanyaan Bisnis No.1
    with tabs[0]:
        # Menampilkan grafik PM2.5 dengan container dan expander
        with st.container():
            st.subheader("PM2.5 Variation over Time")
            # Menambahkan label bahwa ini adalah jawaban untuk pertanyaan bisnis No.1
            # st.markdown("**Menjawab Pertanyaan Bisnis No.1**")
            plot_pm25_over_time(combined_df, style, palette)
            with st.expander("Penjelasan PM2.5 Variation over Time"):
                st.write("""
                    - Kedua stasiun menunjukkan pola musiman yang berbeda dalam tingkat polusi baik PM2.5 maupun PM10. Stasiun Aotizhongxin umumnya mengalami puncak polusi pada awal tahun (Maret) dan akhir tahun (November), sedangkan stasiun Changping cenderung mengalami puncak polusi pada pertengahan tahun (Oktober). 
                    - Secara keseluruhan, kualitas udara di stasiun Aotizhongxin lebih buruk dibandingkan dengan stasiun Changping, ditunjukkan oleh tingkat PM2.5 dan PM10 yang lebih tinggi.
                """)

        # Menampilkan grafik PM10 dengan container dan expander
        with st.container():
            st.subheader("PM10 Variation over Time")
            # Menambahkan label bahwa ini adalah jawaban untuk pertanyaan bisnis No.1
            # st.markdown("**Menjawab Pertanyaan Bisnis No.1**")
            plot_pm10_over_time(combined_df, style, palette)
            with st.expander("Penjelasan PM10 Variation over Time"):
                st.write("""
                    - Kedua stasiun menunjukkan pola musiman yang berbeda dalam tingkat polusi baik PM2.5 maupun PM10. Stasiun Aotizhongxin umumnya mengalami puncak polusi pada awal tahun (Maret) dan akhir tahun (November), sedangkan stasiun Changping cenderung mengalami puncak polusi pada pertengahan tahun (Oktober). 
                    - Secara keseluruhan, kualitas udara di stasiun Aotizhongxin lebih buruk dibandingkan dengan stasiun Changping, ditunjukkan oleh tingkat PM2.5 dan PM10 yang lebih tinggi.
                """)

        # Menampilkan grafik Average Monthly PM2.5 dengan container dan expander
        with st.container():
            st.subheader("Average Monthly PM2.5 Levels by Station")
            plot_average_monthly_pm25(combined_df, style, palette)
            with st.expander("Penjelasan Average Monthly PM2.5 Levels by Station"):
                st.write("""
                    - Kedua stasiun menunjukkan pola musiman yang berbeda dalam tingkat polusi baik PM2.5 maupun PM10. Stasiun Aotizhongxin umumnya mengalami puncak polusi pada awal tahun (Maret) dan akhir tahun (November), sedangkan stasiun Changping cenderung mengalami puncak polusi pada pertengahan tahun (Oktober). 
                    - Secara keseluruhan, kualitas udara di stasiun Aotizhongxin lebih buruk dibandingkan dengan stasiun Changping, ditunjukkan oleh tingkat PM2.5 dan PM10 yang lebih tinggi.
                """)

        # Menampilkan grafik Average Monthly PM10 dengan container dan expander
        with st.container():
            st.subheader("Average Monthly PM10 Levels by Station")
            plot_average_monthly_pm10(combined_df, style, palette)
            with st.expander("Penjelasan Average Monthly PM10 Levels by Station"):
                st.write("""
                    - Kedua stasiun menunjukkan pola musiman yang berbeda dalam tingkat polusi baik PM2.5 maupun PM10. Stasiun Aotizhongxin umumnya mengalami puncak polusi pada awal tahun (Maret) dan akhir tahun (November), sedangkan stasiun Changping cenderung mengalami puncak polusi pada pertengahan tahun (Oktober). 
                    - Secara keseluruhan, kualitas udara di stasiun Aotizhongxin lebih buruk dibandingkan dengan stasiun Changping, ditunjukkan oleh tingkat PM2.5 dan PM10 yang lebih tinggi.
                """)

        # Menampilkan grafik Average Seasonal PM2.5 dengan container dan expander
        with st.container():
            st.subheader("Average Seasonal PM2.5 Levels by Station")
            plot_average_seasonal_pm25(combined_df, style, palette)
            with st.expander("Penjelasan Average Seasonal PM2.5 Levels by Station"):
                st.write("""
                    - Kedua stasiun menunjukkan pola musiman yang berbeda dalam tingkat polusi baik PM2.5 maupun PM10. Stasiun Aotizhongxin umumnya mengalami puncak polusi pada awal tahun (Maret) dan akhir tahun (November), sedangkan stasiun Changping cenderung mengalami puncak polusi pada pertengahan tahun (Oktober). 
                    - Secara keseluruhan, kualitas udara di stasiun Aotizhongxin lebih buruk dibandingkan dengan stasiun Changping, ditunjukkan oleh tingkat PM2.5 dan PM10 yang lebih tinggi.
                """)

        # Menampilkan grafik Average Seasonal PM10 dengan container dan expander
        with st.container():
            st.subheader("Average Seasonal PM10 Levels by Station")
            plot_average_seasonal_pm10(combined_df, style, palette)
            with st.expander("Penjelasan Average Seasonal PM10 Levels by Station"):
                st.write("""
                    - Kedua stasiun menunjukkan pola musiman yang berbeda dalam tingkat polusi baik PM2.5 maupun PM10. Stasiun Aotizhongxin umumnya mengalami puncak polusi pada awal tahun (Maret) dan akhir tahun (November), sedangkan stasiun Changping cenderung mengalami puncak polusi pada pertengahan tahun (Oktober). 
                    - Secara keseluruhan, kualitas udara di stasiun Aotizhongxin lebih buruk dibandingkan dengan stasiun Changping, ditunjukkan oleh tingkat PM2.5 dan PM10 yang lebih tinggi.
                """)

    # Tab untuk Pertanyaan Bisnis No.2
    with tabs[1]:
        # Menampilkan grafik Korelasi antara Cuaca dan Polusi dengan container dan expander
        with st.container():
            st.subheader(
                "Correlation between Weather Conditions and Pollution Levels")
            # Menambahkan label bahwa ini adalah jawaban untuk pertanyaan bisnis No.2
            # st.markdown("**Menjawab Pertanyaan Bisnis No.2**")
            plot_correlation_heatmap(combined_df, style, palette)
            with st.expander("Penjelasan Correlation Heatmap"):
                st.write("""
                    - Menunjukkan hubungan yang sangat kuat antara konsentrasi PM2.5 dan PM10. Artinya, ketika tingkat PM2.5 meningkat, maka tingkat PM10 juga cenderung meningkat, dan sebaliknya. Hal ini menunjukkan bahwa kedua polutan ini seringkali berasal dari sumber yang sama atau dipengaruhi oleh faktor yang sama.
                    - Ketika suhu meningkat, tekanan udara cenderung menurun.
                """)

    # Tab untuk Kesimpulan
    with tabs[2]:
        st.subheader("Kesimpulan")
        st.write("""
            Analisis data kualitas udara di stasiun Aotizhongxin dan Changping menunjukkan adanya perbedaan pola musiman yang signifikan antara kedua lokasi. Stasiun Aotizhongxin umumnya mengalami puncak polusi pada awal dan akhir tahun, sementara Changping pada pertengahan tahun. Secara keseluruhan, kualitas udara di Aotizhongxin lebih buruk dibandingkan Changping. Selain itu, terdapat korelasi yang sangat kuat antara konsentrasi PM2.5 dan PM10, mengindikasikan adanya sumber polusi yang sama atau faktor yang sama yang memengaruhi keduanya. Korelasi negatif antara suhu dan tekanan udara juga ditemukan, yang merupakan fenomena meteorologi umum. Variasi dalam distribusi konsentrasi berbagai polutan menunjukkan adanya masalah kualitas udara yang perlu diperhatikan, terutama di daerah dengan konsentrasi polutan tinggi atau pola distribusi yang tidak normal.
        """)


if __name__ == '__main__':
    main()
