import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
from helper_functions import *
from plotter import *

WINDOW_SIZE = 120
BATCH_SIZE = 64*4
STRIDE = 1
FORECAST_MINUTES = 60

with pd.HDFStore('dataframes.h5') as store:
    dfs = [store[key] for key in store.keys()]

dfs.sort(key=lambda x: len(x), reverse=True)
testing_data = dfs[:1]
training_data = dfs[1:]

y_raw = pd.read_csv("data/reference_neuron_data.csv", delimiter=',', parse_dates=[0], na_values='0')
y_raw['Datetime'] = pd.to_datetime(y_raw['Datetime'])
y_raw.set_index('Datetime', inplace=True)


model = tf.keras.Sequential([
    tf.keras.layers.Conv1D(filters=16, kernel_size=4, strides=2, input_shape=(WINDOW_SIZE, 11)),
    tf.keras.layers.MaxPooling1D(pool_size=2),
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(32, activation="relu"),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(1, activation="sigmoid")  # Kp index
])

model.summary()


loss_fn = tf.keras.losses.MeanSquaredError()
optimizer = tf.keras.optimizers.Adam()
model.compile(optimizer=optimizer,
              loss=loss_fn,
              metrics=[tf.keras.metrics.MeanAbsoluteError()])


def get_dataset(df, param):
    begin = df.index[0].to_pydatetime()
    end = df.index[-1].to_pydatetime()
    delta_t = dt.timedelta(minutes=WINDOW_SIZE - FORECAST_MINUTES)
    train_y = y_raw.fillna(0).loc[(begin - delta_t):(end - delta_t), param]
    return tf.keras.utils.timeseries_dataset_from_array(
        df.iloc[:, :].fillna(0), train_y, sequence_length=WINDOW_SIZE, sequence_stride=STRIDE, batch_size=BATCH_SIZE
    )


NUM_EPOCHS = 2
for df in training_data:
    dataset = get_dataset(df, "Kp")
    if len(dataset) == 0:
        continue
    model.fit(dataset, epochs=NUM_EPOCHS)


dataset = get_dataset(testing_data[0], "Kp")
model.evaluate(dataset, verbose=2)  # [loss, mean_absolute_error]SS


predictions = model.predict(dataset)
delta_t = dt.timedelta(minutes=WINDOW_SIZE-FORECAST_MINUTES)
begin = testing_data[0].index[0].to_pydatetime()-delta_t
end = testing_data[0].index[-1].to_pydatetime()-delta_t


line_width = 1
plt.figure(figsize=(10, 5), dpi=100)
plt.plot(predictions, label="Predicted Kp", linewidth=line_width, color="green")
plt.plot(list(range(len(testing_data[0]))), y_raw["Kp"][begin:end], label="Actual Kp", linewidth=line_width, color="red")


plt.legend()
plt.show()
