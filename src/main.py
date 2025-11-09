import numpy as np
from dataset.image_generation import train_dataset
from fuzzy.features import extract_fuzzy_features
from PIL import Image


(x_train, y_labels) = train_dataset(10000)
features = [extract_fuzzy_features(img) for img in x_train]

max_val = -1000
min_val = 1000
f_min = None
f_max = None
img = None
print(x_train.shape, len(features), y_labels.shape)
for i,f in enumerate(features):
    if f.holes > max_val:
        f_max = y_labels[i]
        img = x_train[i]
    min_val = min(min_val, f.aspect_ratio)
    max_val = max(max_val, f.aspect_ratio)

print(max_val, min_val)