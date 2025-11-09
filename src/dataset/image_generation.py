import numpy as np

from skimage.transform import resize
from tensorflow.keras.datasets import mnist

IMG_SIZE = 28
THRESHOLD = 255.0


def _check_size(image):
    # Ensure correct shape
    tmp = image
    if image.shape != (IMG_SIZE, IMG_SIZE):
        tmp = resize(image, (IMG_SIZE, IMG_SIZE))
    return tmp


def _get_datasets():
    (X_train, y_train), (X_test, y_test) = mnist.load_data()
    # X_train = X_train / THRESHOLD
    # X_test = X_test / THRESHOLD
    X_train = 255 - X_train 
    X_test = 255 - X_test 
    X_train = np.array(list(map(_check_size, X_train)))
    X_test = np.array(list(map(_check_size, X_test)))
    return (X_train, y_train), (X_test, y_test)


def train_dataset(numbers_count: int = 1000):
    (x_train, y_train), _ = _get_datasets()
    return x_train[:numbers_count], y_train[:numbers_count] 
