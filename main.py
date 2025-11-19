import numpy as np
from src.dataset.image_generation import train_dataset
from src.fuzzy.features import extract_fuzzy_features


(x_train, y_labels) = train_dataset(10000)
features = [extract_fuzzy_features(img) for img in x_train]

max_val = -1000
min_val = 1000
f_min = None
f_max = None
img = None
for i,f in enumerate(features):
    if f.holes > max_val:
        f_max = y_labels[i]
        img = x_train[i]
    min_val = min(min_val, f.holes)
    max_val = max(max_val, f.holes)

print(max_val, min_val)