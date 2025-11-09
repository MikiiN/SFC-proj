import cv2
import numpy as np
from dataclasses import dataclass, field
from skimage.measure import euler_number, label
from skimage import measure, morphology, filters
from scipy import ndimage as ndi

IMG_SIZE = 28
THRESHOLD = 255.0
DEFAULT_GRID_SIZE = 4


@dataclass
class Features:
    mean_intensity: float = 0.0
    std_intensity: float = 0.0
    aspect_ratio: float = 0.0
    zone_intensity: list[float] = field(default_factory=list)
    horizontal_symmetry: float = 0.0
    vertical_symmetry: float = 0.0
    horizontal_projection_variance: float = 0.0
    vertical_projection_variance: float = 0.0
    holes: int = 0


def _global_features(img) -> tuple[float, float]:
    mean_intensity = np.mean(img)
    std_intensity = np.std(img)
    return (mean_intensity, std_intensity)


def _aspect_ratio(img) -> float:
    rows, cols = np.where(img > 0.2)
    if len(rows) > 0:
        height = rows.max() - rows.min() + 1
        width = cols.max() - cols.min() + 1
        aspect_ratio = width / height
    else:
        aspect_ratio = 1.0
    return aspect_ratio


def _zone_intensity(img, grid_size) -> list[float]:
    result = []
    zone_h = img.shape[0] // grid_size
    zone_w = img.shape[1] // grid_size
    for i in range(grid_size):
        for j in range(grid_size):
            zone = img[i*zone_h:(i+1)*zone_h, j*zone_w:(j+1)*zone_w]
            result.append(np.mean(zone))
    return result


def _symmetry(img) -> tuple[float, float]:
    h_sym = 1 - np.mean(np.abs(img - np.fliplr(img)))  # left-right symmetry
    v_sym = 1 - np.mean(np.abs(img - np.flipud(img)))  # top-bottom symmetry
    return (h_sym, v_sym)


def _projection_variance(img) -> tuple[float, float]:
    horiz_proj = np.var(np.sum(img, axis=1))
    vert_proj = np.var(np.sum(img, axis=0))
    return (horiz_proj, vert_proj)


def _holes(img, threshold=64) -> int:
    # Step 2: Binarize (foreground white, background black)
    _, binary = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)

    # Step 3: Find contours and hierarchy
    # cv2.RETR_TREE gives full hierarchy
    contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    num_holes = 0

    if hierarchy is not None:
        hierarchy = hierarchy[0]  # shape (num_contours, 4)
        # Each element is [Next, Previous, First_Child, Parent]
        # Holes are contours that have a parent contour (Parent != -1)
        for i, h in enumerate(hierarchy):
            parent = h[3]
            if parent != -1:
                num_holes += 1

    return num_holes


def extract_fuzzy_features(img, grid_size=DEFAULT_GRID_SIZE) -> Features:
    """
    Extract fuzzy-friendly interpretable features from a single MNIST image.
    Input:
        img: 28x28 numpy array (grayscale 0–1)
        grid_size: number of zones per side 
    Output:
        feature vector (list of floats)
    """
    features = Features()
    
    features.mean_intensity, features.std_intensity = _global_features(img)
    
    features.aspect_ratio = _aspect_ratio(img)
    
    # --- Zoning features (mean intensity in each zone) ---
    features.zone_intensity = _zone_intensity(img, grid_size)

    features.horizontal_symmetry, features.vertical_symmetry = _symmetry(img) 
    
    features.horizontal_projection_variance, features.vertical_projection_variance = _projection_variance(img)

    features.holes = _holes(img)
    
    return features