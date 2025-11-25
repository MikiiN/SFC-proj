import cv2
import numpy as np
from dataclasses import dataclass
from skimage.measure import label, regionprops

IMG_SIZE = 28
THRESHOLD = 128
MAX_INTENSITY = 255

@dataclass
class Features:
    centroid: float = 0.0
    aspect_ratio: float = 0.0
    extent: float = 0.0
    solidity: float = 0.0
    horizontal_symmetry: float = 0.0
    vertical_symmetry: float = 0.0
    holes: int = 0


def _crop_image(img) -> np.array:
    mask = img > 0
    if not mask.any():
        return img
    coords = np.argwhere(mask)
    y0, x0 = coords.min(axis=0)
    y1, x1 = coords.max(axis=0) + 1
    return img[y0:y1, x0:x1]


def _centroids(img) -> float:
    cropped = _crop_image(img)
    total_mass = np.sum(cropped)
    if total_mass == 0:
        return 14.0
    height, width = cropped.shape
    _, y_grid = np.meshgrid(np.arange(width), np.arange(height))
    moment = np.sum(y_grid * cropped)
    return (moment / total_mass) / height


def _aspect_ratio(img) -> float:
    rows, cols = np.nonzero(img)
    if len(rows) == 0:
        return 0.0
    height = np.max(rows) - np.min(rows) + 1
    width = np.max(cols) - np.min(cols) + 1
    return width/height


def _symmetry(img) -> tuple[float, float]:
    total_intensity = np.sum(img)
    if total_intensity == 0:
        return (0, 0)
    
    h_sym = 1 - np.sum(np.abs(img - np.fliplr(img))) / (2*total_intensity)  # left-right symmetry
    v_sym = 1 - np.sum(np.abs(img - np.flipud(img))) / (2*total_intensity) # top-bottom symmetry
    return (h_sym, v_sym)


def _solidity(regions) -> float:
    if not regions:
        return 0.0
    digit = max(regions, key=lambda r: r.area)
    return digit.solidity


def _holes(img) -> int:
    img = MAX_INTENSITY - img
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
    features.aspect_ratio = _aspect_ratio(img)
    features.centroid = _centroids(img)
    
    binary_img = np.array(img > THRESHOLD, dtype=np.uint8)
    labeled_img = label(binary_img)
    
    # Get properties (assuming the digit is the largest region)
    regions = regionprops(labeled_img)
    if not regions:
        return None # Empty image
    
    props = regions[0] # Take the first region found
    
    features.extent = props.extent
    features.solidity = _solidity(regions)
    
    return features