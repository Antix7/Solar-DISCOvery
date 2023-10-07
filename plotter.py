import matplotlib.pyplot as plt
from datetime import timedelta
import pandas as pd

def hourly_timeseries_plot(start_time, end_time, df, column_name):
    # Resample the data to hourly frequency and take the mean
    df_resampled = df.resample('H').mean()
    
    delta_time = end_time - start_time
    hours_difference = delta_time.days * 24
    data = []
    times = []
    
    for nr in range(hours_difference):
        current_time = start_time + timedelta(hours=nr)
        times.append(current_time)
        data.append(df_resampled.loc[current_time, str(column_name)])

    plt.figure(figsize=(10, 1), dpi=300)
    plt.rcParams["font.family"] = "Times New Roman"

    plt.plot(times, data, color='black', linewidth=0.4)
    plt.xlabel('Time', fontsize = 10)
    plt.ylabel(column_name, fontsize = 10)
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=8)
    plt.title(f'Time Series Plot of {column_name}')
    plt.gcf().autofmt_xdate()
    plt.show()

