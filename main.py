import tensorflow as tf

# import mnist dataset
mnist = tf.keras.datasets.mnist

# load data
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# divide data by 255 to normalize
x_train, x_test = x_train / 255.0, x_test / 255.0

# create model
model = tf.keras.models.Sequential([
    # flatten 28x28 image to 1D array of 784 pixels
    tf.keras.layers.Flatten(input_shape=(28, 28)),
    # dense layer with 128 nodes
    tf.keras.layers.Dense(128, activation='relu'),
    # dropout layer
    tf.keras.layers.Dropout(0.2),
    # output layer with 10 nodes
    tf.keras.layers.Dense(10)
])

# compile model
model.compile(optimizer='adam',
                loss=tf.keras.losses.SparseCategoricalCrossentropy(
                    from_logits=True),
                metrics=['accuracy'])

# train model
model.fit(x_train, y_train, epochs=10)

# evaluate model
model.evaluate(x_test, y_test, verbose=2)
