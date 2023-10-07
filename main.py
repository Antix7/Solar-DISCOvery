import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
from helper_functions import *

# conversion of .csv files to pandas dataframe and making one big dataframe of all datasets
df = pd.DataFrame()
for i in range(16, 17):
    print("Reading dsc_fc_summed_spectra_20{}_v01.csv".format(i))
    current_df = pd.read_csv(
        "data/dsc_fc_summed_spectra_20{}_v01.csv".format(i),
        delimiter=',',
        parse_dates=[0],
        na_values='0',
        header=None
    )
    if i == 16:
        df = current_df
    else:
        df = pd.concat([df, current_df], ignore_index=True)


# Sets rows index to 'Datetime_UTC'
df.set_index(0, inplace=True)
df.index.name = 'Datetime_UTC'

# Sets columns indexes
magnetic_field_cols = ["Magnetic_Field_GSE_X", "Magnetic_Field_GSE_Y", "Magnetic_Field_GSE_Z"]
spectrum_cols = [f"Raw_Spectrum_{i}" for i in range(1, 51)]
df.columns = magnetic_field_cols + spectrum_cols

Bz = np.array([])
date = dt.datetime(2016, 7, 1, 0, 0)
while date < dt.datetime(2016, 8, 1, 0, 0):
    Bz = np.append(Bz, gse_to_gsm(
        (df.loc[date, 'Magnetic_Field_GSE_X'],
         df.loc[date, 'Magnetic_Field_GSE_Y'],
         df.loc[date, 'Magnetic_Field_GSE_Z']),
        date))
    date += dt.timedelta(minutes=1)

# take a walking average over a window of 1 hour
Bz = np.convolve(Bz, np.ones(60)/60, mode='same')

plt.plot(Bz)
plt.show()
