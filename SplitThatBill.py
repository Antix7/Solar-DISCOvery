import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt

# reading.csv file
df = pd.read_csv("C:\\Users\\zegar\\Desktop\\PytonGigant\\data\\processed_data_interpolated.csv")
df.drop(columns=['Flux_sum'], inplace=True)

df['Datetime_UTC'] = pd.to_datetime(df['Datetime_UTC'])
df.set_index('Datetime_UTC', inplace=True)

# Create a boolean series indicating if the row is all NaNs
is_nan_row = df.isna().all(axis=1)

# Create a helper series that increments when transitioning from NaN to non-NaN and vice versa
helper_series = (is_nan_row != is_nan_row.shift()).cumsum()

# Group by the helper series and create a list of dataframes without all-NaN groups
dfs = [group for _, group in df.groupby(helper_series) if not group.isna().all().all()]

# Clean up the original dataframe (you can skip this if you want to keep the helper columns)
df.drop(columns=['all_nan', 'shifted', 'start_seq', 'end_seq'], errors='ignore', inplace=True)

# Check results
for sub_df in dfs:
    print(sub_df)
    print("-" * 50)

# Find the largest dataframe
largest_df = max(dfs, key=len)

# Print its size and a preview
print(f"The largest dataframe has {len(largest_df)} rows.")
print(largest_df.head())  # this prints the first 5 rows; adjust as needed for more or less

with pd.HDFStore('dataframes.h5') as store:
    for idx, df in enumerate(dfs):
        store[f'df_{idx}'] = df
