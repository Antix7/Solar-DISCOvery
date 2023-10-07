import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt

# Importing and reading .lst files to get Bz, Kp, and Dst data
# Data is indexed by 'Hour' from 2016.07.01 to 2023.05.01
df = pd.read_csv('C:\\Users\\zegar\\Desktop\\PytonGigant\\Solar-DISCOvery\\data\\omni2_Qhtwf1siSe.lst', delim_whitespace=True, header=None)
df.columns = ['Year', 'Day_of_Year', 'Hour', 'Bz_GSM', 'Kp*10', 'Dst_index']
df['Datetime'] = pd.to_datetime(df['Year'].astype(str) + df['Day_of_Year'].astype(str) + df['Hour'].astype(str), format='%Y%j%H')
df.set_index('Datetime', inplace=True)
df.drop(columns=['Year', 'Day_of_Year', 'Hour', 'Bz_GSM'], inplace=True)

# Averaging duplicate rows based on the 'Datetime' index
df = df.groupby(df.index).mean()

# Resample to minute frequency and interpolate
df_minute = df.resample('T').asfreq()
df_reference = df_minute.interpolate(method='linear')

print(df_reference)

# Divide the 'Kp*10' column by 10
df_reference['Kp*10'] = df_reference['Kp*10'] / 10

# Rename the column to 'Kp'
df_reference.rename(columns={'Kp*10': 'Kp'}, inplace=True)

# Drop data after 2023-05-01
df_reference = df_reference[df_reference.index <= '2023-05-01']

# converts all vaules to -1:1
df_neurons = df_reference[['Kp', 'Dst_index']]
df_neurons['Kp'] = df_neurons['Kp'] / 10
# Modify Dst_index column values
df_neurons['Dst_index'] = df_neurons['Dst_index'] / 200

# Clip values to range -1 to 1
df_neurons['Dst_index'] = np.clip(df_neurons['Dst_index'], -1, 1)