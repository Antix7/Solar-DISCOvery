import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


data = pd.read_csv(
    "dsc_fc_summed_spectra_2023_v01.csv",
     delimiter = ',', 
     parse_dates=[0], 
     na_values='0', 
     header = None
)

