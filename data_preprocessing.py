import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
from helper_functions import *
from plotter import *

FLUX_SCALE_FACTOR = 1500
BZ_SCALE_FACTOR = 40


# conversion of .csv files to pandas dataframe and making one big dataframe of all datasets
df = pd.DataFrame()
for i in range(16, 24):
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
spectrum_cols = [f"Raw_Spectrum_{i}" for i in range(50)]
df.columns = magnetic_field_cols + spectrum_cols
# cut off rows before 01.07.2016
df = df.loc['2016-07-01':]


output_df = pd.DataFrame()

print("Adding Bz column...")
output_df['Bz'] = df.apply(lambda row: min(BZ_SCALE_FACTOR, max(-BZ_SCALE_FACTOR,
    gse_to_gsm(
    (row['Magnetic_Field_GSE_X'], row['Magnetic_Field_GSE_Y'], row['Magnetic_Field_GSE_Z']),
    row.name)[2]))/BZ_SCALE_FACTOR, axis=1)

for i in range(10):
    print(f"Adding Spectrum_Sum_{i} column...")
    # Extract relevant columns and calculate mean in a vectorized way
    subset_cols = spectrum_cols[5*i:5*i+5]
    output_df[f"Spectrum_Sum_{i}"] = np.minimum(FLUX_SCALE_FACTOR, np.maximum(-FLUX_SCALE_FACTOR,
        np.mean(df[subset_cols].values, axis=1)
    )) / FLUX_SCALE_FACTOR


valid_rows = ~(
    np.isnan(output_df['Bz']) | np.isnan(output_df.iloc[:, 1:]).all(axis=1)
)
output_df = output_df.loc[valid_rows]

#print minimum values of spectrum columns
print(output_df.iloc[:, 1:].min())
print(output_df.iloc[:, 1:].max())

# print(output_df.head())
# print(output_df.tail())

output_df.to_csv("data/processed_data.csv")

