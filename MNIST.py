import sys; args = sys.argv[1:]
import numpy as np
import keras
from keras.datasets import mnist
from keras.models import Model, Sequential
from keras.layers import Dense, Input
from keras.layers import Conv2D, MaxPooling2D, Dropout, Flatten
from keras.utils import to_categorical
from keras import backend as k
import time
start = time.process_time()

(x_train, y_train), (x_test, y_test) = mnist.load_data()

y_train_encoded = to_categorical(y_train)
y_test_encoded = to_categorical(y_test)

x_train_norm = (x_train/255) - 0.5
x_test_norm = (x_test/255) - 0.5

x_train_images = x_train_norm.reshape((-1, 784))
x_test_images = x_test_norm.reshape((-1, 784))

model = Sequential()
model.add(Dense(64, input_dim = 784, activation = "relu"))
model.add(Dense(32, activation = "relu"))
model.add(Dense(10, activation = "softmax"))

model.compile(optimizer=keras.optimizers.Adadelta(), loss=keras.losses.categorical_crossentropy, metrics=['accuracy'])
model.summary()

model.fit(x_train_images, y_train_encoded, epochs=20, batch_size=10)

scores = model.evaluate(x_test_images, y_test_encoded)
print(scores[1]*100)

print(abs(time.process_time() - start))

model.save_weights('mnistmodel.h5')
model.load_weights('mnistmodel.h5')