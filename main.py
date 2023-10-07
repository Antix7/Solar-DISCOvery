import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
from helper_functions import *
from plotter import *

# import data from csv file
df = pd.read_csv("data/processed_data.csv", delimiter=',', parse_dates=[0], na_values='0')

# print min values of spectrum columns
# print(df.iloc[:, 1:].min())
# print(df.iloc[:, 1:].max())

# # plot column Bz using matplotlib
# plt.plot(df['Datetime_UTC'], df['Bz'])
# plt.show()

plt.plot(df['Datetime_UTC'], df.iloc[:, 1:11])
plt.show()

