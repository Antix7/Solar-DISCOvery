import tensorflow as tf

#create np array with digits 0, 1, 2... to 10
x_train = tf.constant([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
y_train = tf.constant([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])


dataset = tf.keras.utils.timeseries_dataset_from_array(
    x_train, y_train, sequence_length=3, sequence_stride=1, batch_size=4
)
# print the content of the dataset
for batch in dataset:
    inputs, target = batch
    print("Input:", inputs.numpy(), "Target:", target.numpy())
