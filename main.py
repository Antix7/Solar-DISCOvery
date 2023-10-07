import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

##Reads CSV
df = pd.read_csv(
    "dsc_fc_summed_spectra_2023_v01.csv",
     delimiter = ',', 
     parse_dates=[0], 
     na_values='0', 
     header = None
)

##Sets rows index to 'Datetime_UTC'
df.set_index(0, inplace=True)
df.index.name = 'Datetime_UTC'

##Sets columns indexes
magnetic_field_cols = ["Magnetic_Field_GSE_X", "Magnetic_Field_GSE_Y", "Magnetic_Field_GSE_Z"]
spectrum_cols = [f"Raw_Spectrum_{i}" for i in range(1, 51)]
df.columns = magnetic_field_cols + spectrum_cols

print(df.head())
