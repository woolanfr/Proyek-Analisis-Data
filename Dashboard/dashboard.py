import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

def create_sum_sharing(df):
    sumshare_df = df.resample(rule='D', on='dteday').agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum",
        "temp": "mean"  # Menghitung rata-rata suhu
    })
    sumshare_df = sumshare_df.reset_index()
    return sumshare_df

def create_yearly_sharing(df):
    yearlyshare_df = df.resample(rule='Y', on='dteday').agg({
        "casual": "sum",
        "registered": "sum",
        "cnt": "sum",
        "temp": "mean"  # Menghitung rata-rata suhu per tahun
    })
    yearlyshare_df.index = yearlyshare_df.index.strftime('%Y')
    yearlyshare_df.reset_index(inplace=True)  
    return yearlyshare_df

clean_df = pd.read_csv("https://raw.githubusercontent.com/woolanfr/Proyek-Analisis-Data/main/Dashboard/main_data.csv")
clean_df["dteday"] = pd.to_datetime(clean_df["dteday"])

min_date = clean_df["dteday"].min()
max_date = clean_df["dteday"].max()

with st.sidebar:
    st.subheader("Filter data")
    start_date, end_date = st.date_input(
        label='Time span',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = clean_df[(clean_df["dteday"] >= str(start_date)) &
                   (clean_df["dteday"] <= str(end_date))]

sumsharing_df = create_sum_sharing(main_df)
yearlysum_df = create_yearly_sharing(main_df)

st.header("Bike Sharing Dataset")

# Grafik pengaruh temperature terhadap jumlah penyewa sepeda
st.subheader("Influence of Temperature on Bike Rentals")
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(main_df['temp'], main_df['cnt'], color='blue', alpha=0.5)
ax.set_xlabel('Temperature (C)')
ax.set_ylabel('Total Bike Rentals')
ax.set_title('Influence of Temperature on Bike Rentals')
plt.tight_layout()
st.pyplot(fig)

# Grafik jumlah total penyewa sepeda dalam setahun
st.subheader("Total Bike Rentals per Year")
fig, ax = plt.subplots(figsize=(10, 6))
x = np.arange(len(yearlysum_df))
ax.plot(x, yearlysum_df['cnt'], marker='o', label='Total')
ax.plot(x, yearlysum_df['casual'] + yearlysum_df['registered'], marker='o', label='Casual + Registered')
ax.set_xticks(x)
ax.set_xticklabels(yearlysum_df['dteday'], rotation=45, ha='right')
ax.legend(loc='upper left')
ax.set_ylabel('Total Bike Rentals')
ax.set_xlabel('Year')
plt.tight_layout()
st.pyplot(fig)
