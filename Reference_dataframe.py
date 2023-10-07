import pandas as pd
import numpy as np
import datetime as dt

# Importing and reading .lst files to get Bz, Kp, and Dst data
# Data is indexed by 'Hour' from 2016.07.01 to 2023.05.01
df = pd.read_csv('data/omni2_Qhtwf1siSe.lst', delim_whitespace=True, header=None)
df.columns = ['Year', 'Day_of_Year', 'Hour', 'Bz_GSM', 'Kp*10', 'Dst_index']
df['Datetime'] = pd.to_datetime(df['Year'].astype(str) + df['Day_of_Year'].astype(str) + df['Hour'].astype(str), format='%Y%j%H')
df.set_index('Datetime', inplace=True)
df.drop(columns=['Year', 'Day_of_Year', 'Hour'], inplace=True)

# Remove duplicate rows based on the 'Datetime' index
df = df[~df.index.duplicated(keep='first')]

# Resample to minute frequency and interpolate
df_reference = df.resample('T').asfreq()
df_reference = df_reference.interpolate(method='linear')

print(df_reference)

