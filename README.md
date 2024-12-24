# Air Quality Analysis Project

## Overview

This project presents a comprehensive analysis of air quality data collected from various monitoring stations over a period of several years. The analysis aims to address key business questions related to air pollution trends, patterns, and impacts, providing actionable insights for stakeholders to make informed decisions regarding environmental policies and public health initiatives.

The analysis was conducted using Python, leveraging powerful data manipulation and visualization libraries. The results are showcased through an interactive dashboard built with Streamlit, allowing users to explore the findings dynamically.

## Dataset Description

The dataset used in this project, `df_imputed`, contains hourly air quality and weather measurements collected from multiple monitoring stations between **March 1, 2013** and **February 28, 2017**. The dataset has been preprocessed to handle missing values and ensure data integrity.

### Data Structure

- **Index:**
  - `datetime`: Timestamp of each observation, set as the index of the DataFrame.

- **Columns:**
  1. **No** (`int64`): Sequential identifier for each record.
  2. **year** (`int64`): Year of the observation.
  3. **month** (`int64`): Month of the observation.
  4. **day** (`int64`): Day of the observation.
  5. **hour** (`int64`): Hour of the observation.
  6. **PM2.5** (`float64`): Concentration of PM2.5 particles (µg/m³).
  7. **PM10** (`float64`): Concentration of PM10 particles (µg/m³).
  8. **SO2** (`float64`): Sulfur dioxide concentration (µg/m³).
  9. **NO2** (`float64`): Nitrogen dioxide concentration (µg/m³).
  10. **CO** (`float64`): Carbon monoxide concentration (µg/m³).
  11. **O3** (`float64`): Ozone concentration (µg/m³).
  12. **TEMP** (`float64`): Temperature (°C).
  13. **PRES** (`float64`): Atmospheric pressure (hPa).
  14. **DEWP** (`float64`): Dew point (°C).
  15. **RAIN** (`float64`): Rainfall (mm).
  16. **wd** (`category`): Wind direction.
  17. **WSPM** (`float64`): Wind speed (m/s).
  18. **station** (`category`): Monitoring station identifier.
  19. **season** (`object`): Season of the observation (e.g., Spring, Summer).

## Business Questions and Analysis Summary

The analysis was structured to answer the following seven business questions:

1. **What is the distribution of air pollutants across different monitoring stations?**
   - **Analysis:** Conducted univariate and comparative analyses using histograms, boxplots, and descriptive statistics to understand pollutant concentrations across stations.

2. **Are there any seasonal trends in air pollution levels?**
   - **Analysis:** Performed temporal analysis to identify patterns and variations in pollutant levels across different seasons using line plots and bar charts.

3. **How do weather parameters influence air pollutant concentrations?**
   - **Analysis:** Explored correlations between weather variables (e.g., temperature, wind speed) and pollutant levels using heatmaps and scatter plots.

4. **What are the peak pollution periods throughout the year?**
   - **Analysis:** Identified peak pollution times by analyzing hourly and daily pollutant concentrations, highlighting periods of high pollution.

5. **Is there a trend or pattern in pollutant levels over the years?**
   - **Analysis:** Resampled the data monthly to calculate average pollutant levels and visualized trends over the years using line plots.

6. **Which stations are most frequently experiencing high pollution levels?**
   - **Analysis:** Conducted an RFM-like analysis to evaluate Recency, Frequency, and Monetary metrics, identifying stations with recurrent high pollution events.

7. **Are there any anomalies or extreme pollution events in the dataset?**
   - **Analysis:** Utilized Z-Score methods to detect and visualize outlier pollution events, assessing their frequency and impact.

### Key Findings

- **Seasonal Variations:** Certain pollutants, such as PM2.5 and PM10, exhibit higher concentrations during specific seasons, indicating seasonal influences on air quality.
- **Weather Impact:** Strong correlations were observed between wind speed and pollutant dispersion, as well as temperature and ozone levels.
- **Station Performance:** The RFM-like analysis revealed that some stations consistently maintain lower pollution levels, while others frequently experience high pollution events.
- **Trend Analysis:** Over the years, there has been a noticeable trend in the fluctuation of pollutant levels, with certain pollutants showing gradual improvement or worsening.
- **Anomaly Detection:** Several extreme pollution events were identified, which could be attributed to industrial activities or unfavorable weather conditions.

## Installation

To set up the project environment, follow these steps:

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/air-quality-analysis.git
   cd air-quality-analysis
   ```

2. **Create a Virtual Environment**

   It's recommended to use a virtual environment to manage dependencies.

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   Install the required Python packages using `requirements.txt`.

   ```bash
   pip install -r requirements.txt
   ```

## Usage

The analysis results are presented through an interactive dashboard built with Streamlit. To run the dashboard, use the following command:

```bash
streamlit run dashboard/dashboard.py
```

This will launch the dashboard in your default web browser, allowing you to explore the analysis results interactively.

### Dashboard Features

- **Overview:** Summary of key metrics and insights from the dataset.
- **Pollutant Distribution:** Visualizations showing the distribution of various pollutants across stations.
- **Seasonal Trends:** Interactive charts displaying how pollutant levels vary with seasons.
- **Weather Impact:** Correlation plots illustrating the relationship between weather parameters and pollutant concentrations.
- **Trend Analysis:** Line charts depicting pollutant trends over the analyzed years.

## Project Structure

```
air-quality-analysis/
├── dashboard/
│   └── dashboard.py
├── data/
│   └── df_imputed.csv
├── requirements.txt
├── README.md
└── LICENSE
```

- **dashboard/**: Contains the Streamlit dashboard application.
- **data/**: Directory for dataset files.
- **requirements.txt**: Lists all Python dependencies required for the project.
- **README.md**: This file.
- **LICENSE**: Licensing information.

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. **Fork the Repository**
2. **Create a Feature Branch**

   ```bash
   git checkout -b feature/YourFeature
   ```

3. **Commit Your Changes**

   ```bash
   git commit -m "Add YourFeature"
   ```

4. **Push to the Branch**

   ```bash
   git push origin feature/YourFeature
   ```

5. **Open a Pull Request**
