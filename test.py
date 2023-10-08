import tensorflow as tf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# import data/processed_data_interpolated.csv
df = pd.read_csv("data/processed_data_interpolated.csv", delimiter=',', parse_dates=[0], na_values='0')
# replace nan with 0
df.fillna(0, inplace=True)

#plot columns Spectrum_Sum_0 to Spectrum_Sum_9 on a single plot
df.plot(y=['Spectrum_Sum_0', 'Spectrum_Sum_1', 'Spectrum_Sum_2', 'Spectrum_Sum_3', 'Spectrum_Sum_4', 'Spectrum_Sum_5', 'Spectrum_Sum_6', 'Spectrum_Sum_7', 'Spectrum_Sum_8', 'Spectrum_Sum_9'], figsize=(20, 10), title='Spectrum_Sum_0 to Spectrum_Sum_9')
plt.show()


