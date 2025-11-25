import numpy as np
from src.dataset.image_generation import train_dataset
from src.fuzzy.features import extract_fuzzy_features


(x_train, y_labels) = train_dataset(1000)
features = [extract_fuzzy_features(img) for img in x_train]

# max_val = -1000
# min_val = 1000
# f_min = None
# f_max = None
# img = None
# for i,f in enumerate(features):
#     if f.holes > max_val:
#         f_max = y_labels[i]
#         img = x_train[i]
#     min_val = min(min_val, f.holes)
#     max_val = max(max_val, f.holes)

# print(max_val, min_val)


# from sklearn.cluster import KMeans

# centroids = [f.centroid for f in features]
# a_ratios = [f.aspect_ratio for f in features]
# extents = [f.extent for f in features]
# solidities = [f.solidity for f in features]
# h_syms = [f.horizontal_symmetry for f in features]
# v_syms = [f.vertical_symmetry for f in features]
# holes = [f.holes for f in features]


# features_list = [
#     ("centroid", np.array(centroids).reshape(-1,1)), ("aspect_ratio", np.array(a_ratios).reshape(-1,1)), ("extent", np.array(extents).reshape(-1,1)), ("solidity", np.array(solidities).reshape(-1,1)), ("horiz_sym", np.array(h_syms).reshape(-1,1)), ("vertic_sym", np.array(v_syms).reshape(-1,1))
# ]
# for (name, f) in features_list:
#     k_means = KMeans(n_clusters=3, n_init=10, random_state=42)
#     k_means.fit(f)
#     centers = sorted(k_means.cluster_centers_.flatten())
#     print(f"{name}: {centers}")

# print(np.max(np.array(holes)))


from src.optimization.gen_alg import optimize

optimize(x_train, y_labels)