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

# import data from csv file
nrows = 1000000
x_raw = pd.read_csv("data/processed_data_interpolated.csv", delimiter=',', parse_dates=[0], na_values='0')
y_raw = pd.read_csv("data/reference_neuron_data.csv", delimiter=',', parse_dates=[0], na_values='0')

x_raw = x_raw.iloc[:, 1:-1].fillna(0)
y_raw = y_raw.iloc[:, 1:].fillna(0)

# cut off first rows from y_raw
y_raw = y_raw.iloc[(FORECAST_MINUTES+WINDOW_SIZE):, :]
# cut off last rows from x_raw
x_raw = x_raw.iloc[:-(FORECAST_MINUTES+WINDOW_SIZE), :]

# print(x_raw.shape, y_raw.shape)


def get_dataset(a=0, b=-1):
    return tf.keras.utils.timeseries_dataset_from_array(
        x_raw[a:b], y_raw["Kp"][a:b], sequence_length=WINDOW_SIZE, sequence_stride=STRIDE, batch_size=BATCH_SIZE
    )


TRAIN_SIZE = 500000
TEST_SIZE = 200000
train_dataset = get_dataset(0, TRAIN_SIZE)
test_dataset = get_dataset(TRAIN_SIZE, TRAIN_SIZE+TEST_SIZE)


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

model.fit(train_dataset, epochs=5)

model.evaluate(test_dataset, verbose=2)

# make predictions for first batch of test data
predictions = model.predict(test_dataset)


line_width = 0.75
plt.plot(predictions, label="Predicted Kp", linewidth=line_width)
plt.plot(list(range(TEST_SIZE)), y_raw["Kp"][TRAIN_SIZE:TRAIN_SIZE+TEST_SIZE], label="Actual Kp", linewidth=line_width)


plt.legend()
plt.show()
