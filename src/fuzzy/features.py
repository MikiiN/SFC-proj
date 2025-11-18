import cv2
import numpy as np
from dataclasses import dataclass, field
from skimage.measure import label, regionprops

IMG_SIZE = 28
THRESHOLD = 128


@dataclass
class Features:
    centroid: float = 0.0
    aspect_ratio: float = 0.0
    extent: float = 0.0
    solidity: float = 0.0
    horizontal_symmetry: float = 0.0
    vertical_symmetry: float = 0.0
    holes: int = 0


def _centroids(img, props) -> float:
    cy, _ = props.centroid
    return cy / img.shape[0] 


def _aspect_ratio(props) -> float:
    min_r, min_c, max_r, max_c = props.bbox
    height = max_r - min_r
    width = max_c - min_c
    return width / height if height > 0 else 0


def _symmetry(img) -> tuple[float, float]:
    h_sym = 1 - np.mean(np.abs(img - np.fliplr(img)))  # left-right symmetry
    v_sym = 1 - np.mean(np.abs(img - np.flipud(img)))  # top-bottom symmetry
    return (h_sym, v_sym)


def _solidity(regions) -> float:
    if not regions:
        return 0.0
    digit = max(regions, key=lambda r: r.area)
    return digit.solidity


def _holes(img) -> int:
    # Find connected components
    num_labels, labels = cv2.connectedComponents(img)

    # Background label (outer) touches border
    # We find all labels touching the border and exclude them.
    border_labels = np.unique(np.concatenate([
        labels[0, :], labels[-1, :], labels[:, 0], labels[:, -1]
    ]))

    # Count holes: all labels minus border components and background
    hole_labels = [l for l in range(1, num_labels) if l not in border_labels]
    return len(hole_labels)


def extract_fuzzy_features(img) -> Features:
    features = Features()
    features.holes = _holes(img)
    features.horizontal_symmetry, features.vertical_symmetry = _symmetry(img) 
    
    binary_img = np.array(img > THRESHOLD, dtype=np.uint8)
    labeled_img = label(binary_img)
    
    # Get properties (assuming the digit is the largest region)
    regions = regionprops(labeled_img)
    if not regions:
        return None # Empty image
    
    props = regions[0] # Take the first region found
    
    features.centroid = _centroids(binary_img, props)
    features.aspect_ratio = _aspect_ratio(props)
    features.extent = props.extent
    features.solidity = _solidity(regions)
    
    return features