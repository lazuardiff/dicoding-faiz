import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np


def process_data(file_path):
    """
    Membaca dan memproses data dari file CSV.

    Parameters:
    - file_path (str): Path ke file CSV.

    Returns:
    - pd.DataFrame: DataFrame yang telah diproses.
    """
    try:
        # Membaca file CSV
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

    # Konversi kolom 'datetime' jika ada
    if 'datetime' in df.columns:
        try:
            df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')
        except Exception as e:
            st.error(
                f"Terjadi kesalahan saat mengonversi kolom 'datetime': {e}")
            st.stop()
    else:
        st.error("Kolom 'datetime' tidak ditemukan dalam dataset.")
        st.stop()

    # Validasi nilai 'datetime'
    invalid_datetime = df['datetime'].isna().sum()
    if invalid_datetime > 0:
        st.warning(
            f"Ada {invalid_datetime} baris dengan nilai 'datetime' tidak valid. Baris ini akan dihapus.")
        df = df.dropna(subset=['datetime'])

    # Mengurutkan DataFrame berdasarkan datetime
    df = df.sort_values(by='datetime').reset_index(drop=True)

    return df


def plot_pm_variation_combined(df, style, palette):
    """
    Membuat visualisasi tren bulanan rata-rata PM2.5 dan PM10 untuk setiap kota.

    Parameters:
    - df (pd.DataFrame): DataFrame yang telah diproses.
    - style (str): Gaya seaborn yang dipilih.
    - palette (str): Palet warna seaborn yang dipilih.
    """
    # Pastikan kolom 'date' tidak menjadi indeks, atau buat ulang kolom 'date'
    if isinstance(df.index, pd.DatetimeIndex):
        df = df.reset_index()

    # Menghitung Rata-rata PM2.5 dan PM10 per Bulan untuk Setiap Kota
    df['datetime'] = pd.to_datetime(
        df[['year', 'month', 'day', 'hour']], errors='coerce')
    # Mengelompokkan berdasarkan periode bulanan
    df['month_year'] = df['datetime'].dt.to_period('M')
    monthly_avg = df.groupby(['station', 'month_year'])[
        ['PM2.5', 'PM10']].mean().reset_index()

    # Konversi kembali 'month_year' ke datetime untuk plotting
    monthly_avg['month_year'] = monthly_avg['month_year'].dt.to_timestamp()

    # Visualisasi
    plt.figure(figsize=(14, 8))
    sns.set_style(style)
    sns.set_palette(palette)

    # PM2.5
    plt.subplot(2, 1, 1)
    sns.lineplot(data=monthly_avg, x='month_year',
                 y='PM2.5', hue='station', marker='o')
    plt.title('Tren Rata-rata Bulanan PM2.5 di Changping dan Aotizhongxin')
    plt.xlabel('Bulan')
    plt.ylabel('PM2.5')
    plt.legend(title='Kota')

    # PM10
    plt.subplot(2, 1, 2)
    sns.lineplot(data=monthly_avg, x='month_year',
                 y='PM10', hue='station', marker='o')
    plt.title('Tren Rata-rata Bulanan PM10 di Changping dan Aotizhongxin')
    plt.xlabel('Bulan')
    plt.ylabel('PM10')
    plt.legend(title='Kota')

    plt.tight_layout()
    st.pyplot(plt.gcf())
    plt.clf()


def plot_weather_pollution_correlation(df, style, palette):
    """
    Membuat visualisasi korelasi antara kondisi cuaca dan tingkat polusi,
    menggunakan heatmap dan scatter plots.

    Parameters:
    - df (pd.DataFrame): DataFrame yang telah diproses.
    - style (str): Gaya seaborn yang dipilih.
    - palette (str): Palet warna seaborn yang dipilih.
    """
    weather_pollutant_cols = ['TEMP', 'PRES', 'WSPM', 'PM2.5', 'PM10']

    # a. Menghitung Matriks Korelasi
    correlation_matrix = df[weather_pollutant_cols].corr()

    # b. Visualisasi Heatmap Korelasi
    plt.figure(figsize=(8, 6))
    sns.set_style(style)
    sns.heatmap(correlation_matrix, annot=True, fmt=".2f",
                cmap='coolwarm', vmin=-1, vmax=1)
    plt.title('Heatmap Korelasi Antara Kondisi Cuaca dan Tingkat Polusi')
    st.pyplot(plt.gcf())
    plt.clf()

    # c. Visualisasi Scatter Plots
    sns.set_palette(palette)
    pairplot_fig = sns.pairplot(
        df, vars=weather_pollutant_cols, hue='station', palette='viridis')
    pairplot_fig.fig.suptitle(
        'Scatter Plots Korelasi Kondisi Cuaca dan Polusi per Kota', y=1.02)
    st.pyplot(pairplot_fig.fig)


def plot_pollutant_correlation(df, style, palette):
    """
    Membuat heatmap korelasi antar polutan udara.

    Parameters:
    - df (pd.DataFrame): DataFrame yang telah diproses.
    - style (str): Gaya seaborn yang dipilih.
    - palette (str): Palet warna seaborn yang dipilih.
    """
    # Pastikan kolom polutan ada di dataset
    pollutant_cols = ['SO2', 'NO2', 'CO', 'O3']
    if not set(pollutant_cols).issubset(df.columns):
        st.error(f"Kolom-kolom {pollutant_cols} tidak ditemukan dalam data.")
        return

    # Menghitung matriks korelasi
    pollutant_corr = df[pollutant_cols].corr()

    # Visualisasi Heatmap
    plt.figure(figsize=(6, 5))
    sns.set_style(style)
    sns.heatmap(pollutant_corr, annot=True, fmt=".2f",
                cmap='coolwarm', vmin=-1, vmax=1)
    plt.title('Heatmap Korelasi Antar Polutan Udara')
    st.pyplot(plt.gcf())
    plt.clf()


def plot_station_pollutant_avg(df, pollutants, style, palette):
    """
    Membuat visualisasi rata-rata konsentrasi polutan per stasiun.

    Parameters:
    - df (pd.DataFrame): DataFrame yang telah diproses.
    - pollutants (list): Daftar nama kolom polutan untuk divisualisasikan.
    - style (str): Gaya seaborn yang dipilih.
    - palette (str): Palet warna seaborn yang dipilih.
    """
    # Pastikan kolom polutan dan 'station' ada di dataset
    if not {'station'}.issubset(df.columns):
        st.error("Kolom 'station' tidak ditemukan dalam data.")
        return
    if not set(pollutants).issubset(df.columns):
        st.error(f"Kolom-kolom {pollutants} tidak ditemukan dalam data.")
        return

    # Menghitung rata-rata konsentrasi polutan per stasiun
    station_pollutant_avg = df.groupby(
        'station')[pollutants].mean().reset_index()

    # Visualisasi
    plt.figure(figsize=(18, 12))
    sns.set_style(style)
    sns.set_palette(palette)

    for i, pol in enumerate(pollutants, 1):
        plt.subplot(2, 3, i)
        sns.barplot(x='station', y=pol,
                    data=station_pollutant_avg, palette='viridis')
        plt.title(f'Rata-rata {pol} per Stasiun')
        plt.xlabel('Stasiun')
        plt.ylabel(pol)
        plt.xticks(rotation=45)

    plt.tight_layout()
    st.pyplot(plt.gcf())
    plt.clf()


def plot_monthly_pollutant_trends(df, pollutant_columns, style="darkgrid",palette="viridis"):
    """
    Membuat plot tren rata-rata bulanan polutan udara sepanjang tahun.

    Parameters:
    - df (pd.DataFrame): DataFrame yang telah diproses.
    - pollutant_columns (list): Daftar nama kolom untuk polutan yang akan dianalisis.
    - palette (str): Palet warna seaborn untuk plot.
    - style (str): Gaya seaborn untuk plot.

    Returns:
    - None
    """
    st.subheader("Tren Rata-rata Bulanan Polutan Udara Sepanjang Tahun")

    # Mengatur gaya seaborn
    sns.set_style(style)
    sns.set_palette(palette)

    # Validasi kolom 'datetime'
    if 'datetime' not in df.columns:
        st.error("Kolom 'datetime' tidak ditemukan dalam dataset.")
        return
    if not pd.api.types.is_datetime64_any_dtype(df['datetime']):
        try:
            df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')
        except Exception as e:
            st.error(f"Error saat mengonversi kolom 'datetime': {e}")
            return

    # Resampling data per bulan dan menghitung rata-rata polutan
    try:
        monthly_pollutant_avg = df.set_index(
            'datetime')[pollutant_columns].resample('M').mean().reset_index()
    except Exception as e:
        st.error(f"Error saat melakukan resampling data: {e}")
        return

    # Membuat plot
    plt.figure(figsize=(14, 10))
    for pol in pollutant_columns:
        plt.plot(monthly_pollutant_avg['datetime'],
                 monthly_pollutant_avg[pol], label=pol)
    plt.title('Tren Rata-rata Bulanan Polutan Udara Sepanjang Tahun')
    plt.xlabel('Bulan')
    plt.ylabel('Konsentrasi Polutan')
    plt.legend()
    plt.grid(True)

    # Menampilkan plot di Streamlit
    st.pyplot(plt.gcf())
    plt.clf()


def plot_station_temperature_stats(df, style="darkgrid", palette="coolwarm"):
    """
    Membuat plot suhu tertinggi dan terendah per stasiun, serta menampilkan informasi
    stasiun dengan suhu tertinggi dan terendah.

    Parameters:
    - df (pd.DataFrame): DataFrame yang telah diproses.
    - palette (str): Palet warna seaborn untuk plot.
    - style (str): Gaya seaborn untuk plot.

    Returns:
    - None
    """
    st.subheader("Suhu Tertinggi dan Terendah per Stasiun")

    # Mengatur gaya seaborn
    sns.set_style(style)
    sns.set_palette(palette)

    # Pastikan kolom 'TEMP' dan 'station' ada
    required_columns = {'TEMP', 'station'}
    if not required_columns.issubset(df.columns):
        st.error(f"Kolom berikut wajib ada dalam dataset: {required_columns}")
        return

    # Menghitung suhu minimum dan maksimum per stasiun
    try:
        station_temp_stats = df.groupby('station')['TEMP'].agg(
            ['min', 'max']).reset_index()
    except Exception as e:
        st.error(f"Error saat menghitung statistik suhu: {e}")
        return

    # Menemukan stasiun dengan suhu terendah dan tertinggi
    try:
        lowest_temp_station = station_temp_stats.loc[station_temp_stats['min'].idxmin(
        )]
        highest_temp_station = station_temp_stats.loc[station_temp_stats['max'].idxmax(
        )]
    except Exception as e:
        st.error(f"Error saat menentukan stasiun dengan suhu ekstrem: {e}")
        return

    # Menampilkan hasil di Streamlit
    st.write(
        f"**Suhu terendah**: {lowest_temp_station['min']}°C di stasiun **{lowest_temp_station['station']}**")
    st.write(
        f"**Suhu tertinggi**: {highest_temp_station['max']}°C di stasiun **{highest_temp_station['station']}**")

    # Visualisasi suhu per stasiun
    try:
        melted_temp = station_temp_stats.melt(
            id_vars='station',
            value_vars=['min', 'max'],
            var_name='Temperature_Type',
            value_name='Temperature'
        )

        plt.figure(figsize=(14, 8))
        sns.barplot(
            x='station',
            y='Temperature',
            hue='Temperature_Type',
            data=melted_temp,
            palette=palette
        )
        plt.title('Suhu Tertinggi dan Terendah per Stasiun')
        plt.xlabel('Stasiun')
        plt.ylabel('Suhu (°C)')
        plt.xticks(rotation=45)
        plt.legend(title='Jenis Suhu')

        # Menampilkan plot di Streamlit
        st.pyplot(plt.gcf())
        plt.clf()
    except Exception as e:
        st.error(f"Error saat membuat visualisasi: {e}")


def plot_highest_rainfall_station(df, style="darkgrid", palette="Blues_d"):
    """
    Membuat plot curah hujan tertinggi per stasiun, serta menampilkan informasi
    stasiun dengan curah hujan tertinggi.

    Parameters:
    - df (pd.DataFrame): DataFrame yang telah diproses.
    - palette (str): Palet warna seaborn untuk plot.
    - style (str): Gaya seaborn untuk plot.

    Returns:
    - None
    """
    st.subheader("Curah Hujan Tertinggi per Stasiun")

    # Mengatur gaya seaborn
    sns.set_style(style)
    sns.set_palette(palette)

    # Pastikan kolom 'RAIN' dan 'station' ada
    required_columns = {'RAIN', 'station'}
    if not required_columns.issubset(df.columns):
        st.error(f"Kolom berikut wajib ada dalam dataset: {required_columns}")
        return

    # Menghitung curah hujan maksimum per stasiun
    try:
        station_rain_max = df.groupby('station')['RAIN'].max().reset_index()
    except Exception as e:
        st.error(f"Error saat menghitung curah hujan maksimum: {e}")
        return

    # Menemukan stasiun dengan curah hujan tertinggi
    try:
        highest_rain_station = station_rain_max.loc[station_rain_max['RAIN'].idxmax(
        )]
    except Exception as e:
        st.error(
            f"Error saat menentukan stasiun dengan curah hujan tertinggi: {e}")
        return

    # Menampilkan hasil di Streamlit
    st.write(
        f"**Curah hujan tertinggi**: {highest_rain_station['RAIN']} mm di stasiun **{highest_rain_station['station']}**"
    )

    # Visualisasi curah hujan per stasiun
    try:
        plt.figure(figsize=(14, 8))
        sns.barplot(
            x='station',
            y='RAIN',
            data=station_rain_max,
            palette=palette
        )
        plt.title('Curah Hujan Tertinggi per Stasiun')
        plt.xlabel('Stasiun')
        plt.ylabel('Curah Hujan (mm)')
        plt.xticks(rotation=45)

        # Menampilkan plot di Streamlit
        st.pyplot(plt.gcf())
        plt.clf()
    except Exception as e:
        st.error(f"Error saat membuat visualisasi: {e}")


def display_filtered_dataframe(df):
    """
    Menampilkan DataFrame dengan filter langsung di dashboard Streamlit.

    Parameters:
    - df (pd.DataFrame): DataFrame yang akan difilter dan ditampilkan.
    """
    st.subheader("Filter DataFrame")

    # Validasi kolom 'datetime'
    if 'datetime' not in df.columns:
        st.error("Kolom 'datetime' tidak ditemukan dalam dataset.")
        return

    # Konversi kolom 'datetime' ke tipe datetime64 jika belum
    if not pd.api.types.is_datetime64_any_dtype(df['datetime']):
        try:
            df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')
        except Exception as e:
            st.error(f"Error saat mengonversi kolom 'datetime': {e}")
            return

    # Filter untuk kolom 'station'
    selected_station = st.multiselect(
        "Pilih Stasiun", df['station'].unique(), default=df['station'].unique()
    )

    # Filter untuk kolom 'year'
    selected_year = st.multiselect(
        "Pilih Tahun", df['year'].unique(), default=df['year'].unique()
    )

    # Filter untuk kolom 'season'
    selected_season = st.multiselect(
        "Pilih Musim", df['season'].unique(), default=df['season'].unique()
    )

    # Slider untuk rentang waktu
    # Konversi ke Python datetime
    min_datetime = df['datetime'].min().to_pydatetime()
    # Konversi ke Python datetime
    max_datetime = df['datetime'].max().to_pydatetime()

    # Validasi nilai minimum dan maksimum
    if pd.isnull(min_datetime) or pd.isnull(max_datetime):
        st.error("Nilai minimum atau maksimum datetime tidak valid.")
        return

    # Slider untuk memilih rentang waktu
    selected_datetime_range = st.slider(
        "Pilih Rentang Waktu",
        min_value=min_datetime,
        max_value=max_datetime,
        value=(min_datetime, max_datetime),
        format="YYYY-MM-DD HH:mm"
    )

    # Menerapkan filter pada DataFrame
    filtered_df = df.copy()
    if selected_station:
        filtered_df = filtered_df[filtered_df['station'].isin(
            selected_station)]
    if selected_year:
        filtered_df = filtered_df[filtered_df['year'].isin(selected_year)]
    if selected_season:
        filtered_df = filtered_df[filtered_df['season'].isin(selected_season)]
    if selected_datetime_range:
        filtered_df = filtered_df[
            (filtered_df['datetime'] >= selected_datetime_range[0]) &
            (filtered_df['datetime'] <= selected_datetime_range[1])
        ]

    # Menampilkan DataFrame yang telah difilter
    st.write(f"Data setelah difilter: {filtered_df.shape[0]} baris")
    st.dataframe(filtered_df)
