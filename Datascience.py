import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt

# reading .csv file
df = pd.read_csv("C:\\Users\\zegar\\Desktop\\PytonGigant\\data\\processed_data.csv")

# Convert Datetime_UTC to datetime type
df['Datetime_UTC'] = pd.to_datetime(df['Datetime_UTC'])

# Set Datetime_UTC as the index
df.set_index('Datetime_UTC', inplace=True)

# Resample dataframe to minute frequency, aggregate by mean if multiple datapoints
df_resampled = df.resample('T').mean()

# Step 1: Identify where data is missing (NaN) 
# by using the 'isna()' method and get the differences in rows 
df_resampled['gap'] = df_resampled.isna().all(axis=1).astype(int).diff()

# Step 2: Group consecutive missing data
start_gaps = df_resampled[df_resampled['gap'] == 1].index
end_gaps = df_resampled[df_resampled['gap'] == -1].index

if len(start_gaps) > len(end_gaps):  # If the last gap goes till the end of the dataset
    end_gaps = end_gaps.insert(len(end_gaps), df_resampled.index[-1])

if len(start_gaps) < len(end_gaps):  # If there's a gap at the beginning of the dataset
    start_gaps = start_gaps.insert(0, df_resampled.index[0])

# ... [Your code above for gap detection remains unchanged]

# Storing gap information
gap_info = []
for start, end in zip(start_gaps, end_gaps):
    gap_length = (end - start).seconds // 60 + 1  # in minutes
    gap_info.append((start, end, gap_length))
    if gap_length > 120:
        print(f"Gap from {start} to {end} of length {gap_length} minutes")


# ... [Everything above remains unchanged until interpolation]

# Drop the 'gap' column before summing
df_resampled.drop(columns=['gap'], inplace=True)

# Interpolating for gaps below 120 minutes on the summed data
for start, end, length in gap_info:
    if length <= 120:
        df_resampled['Bz'].loc[start:end] = df_resampled['Bz'].loc[start:end].interpolate(method='linear', limit_direction='both').bfill().ffill()
        for i in range(10):
            column = f'Spectrum_Sum_{i}'
            df_resampled[column].loc[start:end] = df_resampled[column].loc[start:end].interpolate(method='linear', limit_direction='both').bfill().ffill()

spectrum_cols = [f'Spectrum_Sum_{i}' for i in range(10)]
df_resampled['Flux_sum'] = df_resampled[spectrum_cols].sum(axis=1) / 10


# Plotting the interpolated sum over time
# plt.figure(figsize=(14, 7))  # Adjust the figure size
# plt.plot(df_resampled.index, df_resampled['Flux_sum'], label='Interpolated Sum of Parameters', color='green')
# plt.xlabel('Datetime_UTC')
# plt.ylabel('Sum')
# plt.title('Interpolated Sum of All Parameters Over Time')
# plt.legend()
# plt.grid(True)
# plt.tight_layout()
# plt.show()

df_resampled.to_csv('data/processed_data_interpolated.csv')