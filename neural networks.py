from keras import layers, models
from keras.datasets import mnist
from keras.utils import to_categorical

# Загрузка данных MNIST
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

# Подготовка данных
train_images = train_images.reshape((60000, 28, 28, 1)).astype('float32') / 255
test_images = test_images.reshape((10000, 28, 28, 1)).astype('float32') / 255
train_labels = to_categorical(train_labels)
test_labels = to_categorical(test_labels)

# # Построение модели MLP
# model_mlp = models.Sequential()
# model_mlp.add(layers.Flatten(input_shape=(28, 28, 1)))
# model_mlp.add(layers.Dense(128, activation='relu'))
# model_mlp.add(layers.Dense(10, activation='softmax'))
#
# # Компиляция модели
# model_mlp.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
#
# # Обучение модели
# model_mlp.fit(train_images, train_labels, epochs=10, batch_size=64, validation_split=0.2)
#
# # Оценка модели на тестовых данных
# test_loss, test_acc = model_mlp.evaluate(test_images, test_labels)
# print(f'Test accuracy: {test_acc}')
#

# Построение сверточной нейронной сети (CNN)
model_cnn = models.Sequential()
model_cnn.add(layers.Conv2D(32, (3, 3), activation='relu', input_shape=(28, 28, 1)))
model_cnn.add(layers.MaxPooling2D((2, 2)))
model_cnn.add(layers.Conv2D(64, (3, 3), activation='relu'))
model_cnn.add(layers.MaxPooling2D((2, 2)))
model_cnn.add(layers.Conv2D(64, (3, 3), activation='relu'))
model_cnn.add(layers.Flatten())
model_cnn.add(layers.Dense(64, activation='relu'))
model_cnn.add(layers.Dense(10, activation='softmax'))

# Компиляция CNN
model_cnn.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Обучение CNN
model_cnn.fit(train_images, train_labels, epochs=10, batch_size=64, validation_split=0.2)

# Оценка CNN на тестовых данных
test_loss_cnn, test_acc_cnn = model_cnn.evaluate(test_images, test_labels)
print(f'Test accuracy (CNN): {test_acc_cnn}')
