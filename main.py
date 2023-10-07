import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
from helper_functions import *
from plotter import *

# import data from csv file
df = pd.read_csv("data/processed_data.csv", delimiter=',', parse_dates=[0], na_values='0')

print(df.head())

num_of_gaps = 0
gaps = []
for i in range(1, len(df)):
    if (df.loc[i, 'Datetime_UTC'] - df.loc[i - 1, 'Datetime_UTC']).total_seconds() != 60.0:
        num_of_gaps += 1
        gaps.append([df.loc[i, 'Datetime_UTC'], df.loc[i - 1, 'Datetime_UTC']])
print("Number of gaps: ", num_of_gaps)
