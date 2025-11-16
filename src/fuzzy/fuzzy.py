from src.fuzzy.features import extract_fuzzy_features
import src.fuzzy.fuzzy_sets as fsets

def fuzzification(img):
    features = extract_fuzzy_features(img)
    mean_set = fsets.MeanIntensitySet(features.mean_intensity)
    std_set = fsets.StdIntensitySet(features.std_intensity)
    ratio_set = fsets.AspectRatioSet(features.aspect_ratio)
    zone_sets = [fsets.AspectRatioSet(zone) for zone in features.zone_intensity]
    hsym_set = fsets.SymmetrySet(features.horizontal_symmetry)
    vsym_set = fsets.SymmetrySet(features.vertical_symmetry)
    hole_set = fsets.HoleSet(features.holes)