import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
from helper_functions import *
from plotter import *

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

print("Adding Bz column...")
df['Bz'] = df.apply(lambda row: gse_to_gsm(
    (row['Magnetic_Field_GSE_X'], row['Magnetic_Field_GSE_Y'], row['Magnetic_Field_GSE_Z']),
    row.name)[2], axis=1)

start_date = dt.datetime(2016, 7, 1, 0, 0)
end_date = dt.datetime(2016, 8, 1, 0, 0)
hourly_timeseries_plot(start_date, end_date, df, 'Bz')
