import matplotlib.pyplot as plt
from datetime import timedelta
import pandas as pd

def hourly_timeseries_plot(start_time, end_time, df, column_name):
    # Resample the data to hourly frequency and take the mean
    df_resampled = df.resample('H').mean()
    
    delta_time = end_time - start_time
    data = []
    times = []
    
    for nr in range(delta_time.hour):
        current_time = start_time + timedelta(hours=nr)
        times.append(current_time)
        data.append(df_resampled.loc[current_time, str(column_name)])

    plt.plot(times, data, color='black', linewidth=1, figsize=(2.53, 0.67), dpi=300)
    plt.xlabel('Time')
    plt.ylabel(column_name)
    plt.title(f'Time Series Plot of {column_name}')
    plt.gcf().autofmt_xdate()
    plt.show()

