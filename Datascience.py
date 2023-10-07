import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime as dt

# importing data from .csv file
df = pd.read_csv('data/processed_data.csv')

# Convert to datetime and set as index
df['Datetime_UTC'] = pd.to_datetime(df['Datetime_UTC'])
df.set_index('Datetime_UTC', inplace=True)

# Drop duplicates based on the index (Datetime_UTC)
df = df[~df.index.duplicated(keep='first')]

# Resample to ensure every minute is present
df_resampled = df.resample('T').asfreq()
df_resampled = df_resampled.replace(0, np.nan)

# Linearly interpolate gaps shorter than 2 hours for all columns
df_resampled.interpolate(method='linear', limit=60, limit_direction='both', inplace=True)

# Create a 'missing' column: 1 for missing data and 0 otherwise
df_resampled['missing'] = df_resampled.isnull().all(axis=1).astype(int)

# Compute the sum of flux for every minute and divide by 10
df_resampled['flux_sum'] = df_resampled.drop(columns='missing').sum(axis=1) / 10

# Identify gaps (whole groups of consecutive missing datapoints)
gap_groups = (df_resampled['missing'] != df_resampled['missing'].shift()).cumsum()
gap_counts = df_resampled[df_resampled['missing'] == 1].groupby(gap_groups).size()

# Print the number of gaps and their sizes
print(f"Number of data gaps: {len(gap_counts)}")
print("Sizes of the gaps:", gap_counts.tolist())

# Plotting
plt.figure(figsize=(15, 5))
df_resampled['flux_sum'].plot(label='Interpolated Data', linewidth=1)

# Add scatter plot for missing points
missing_points = df_resampled[df_resampled['missing'] == 1]
plt.scatter(missing_points.index, missing_points['flux_sum'], color='red', s=10, label='Missing Data Points')

plt.title('Linearly Interpolated Minute Flux Sum Data (divided by 10) with Missing Points')
plt.ylabel('Sum of Flux / 10')
plt.xlabel('Datetime')
plt.legend()
plt.tight_layout()
plt.show()
