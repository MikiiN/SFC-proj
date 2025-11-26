import random

def gen_correct_params(
        low_center,
        medium_center,
        high_center,
        center_variance,
        low_variance,
        medium_variance,
        high_variance,
        variance_variance
): 
    while True:
        low_c = random.uniform(low_center-center_variance, low_center+center_variance)
        low_v = random.uniform(low_variance-variance_variance, low_variance+variance_variance)
        medium_c = random.uniform(medium_center-center_variance, medium_center+center_variance)
        medium_v = random.uniform(medium_variance-variance_variance, medium_variance+variance_variance)
        high_c = random.uniform(high_center-center_variance, high_center+center_variance)
        high_v = random.uniform(high_variance-variance_variance, high_variance+variance_variance)
        if low_c < medium_c and medium_c < high_c:
            break
    return low_c, low_v, medium_c, medium_v, high_c, high_v


def gen_correct_centroid_params():
    LOW_CENTER = 0.379
    MEDIUM_CENTER = 0.474
    HIGH_CENTER = 0.559
    C_VARIANCE = 0.1
    VARIANCE = 0.2
    VARIANCE_OF_VARIANCE = 0.15
    return gen_correct_params(
        LOW_CENTER,
        MEDIUM_CENTER,
        HIGH_CENTER,
        C_VARIANCE,
        VARIANCE,
        VARIANCE,
        VARIANCE,
        VARIANCE_OF_VARIANCE
    )


def gen_correct_aspect_ratio_params():
    LOW_CENTER = 0.516
    MEDIUM_CENTER = 0.797
    HIGH_CENTER = 1.059
    C_VARIANCE = 0.1
    VARIANCE = 0.3
    VARIANCE_OF_VARIANCE = 0.2
    return gen_correct_params(
        LOW_CENTER,
        MEDIUM_CENTER,
        HIGH_CENTER,
        C_VARIANCE,
        VARIANCE,
        VARIANCE,
        VARIANCE,
        VARIANCE_OF_VARIANCE
    )


def gen_correct_extent_params():
    LOW_CENTER = 0.288
    MEDIUM_CENTER = 0.414
    HIGH_CENTER = 0.616
    C_VARIANCE = 0.1
    VARIANCE = 0.2
    VARIANCE_OF_VARIANCE = 0.15
    return gen_correct_params(
        LOW_CENTER,
        MEDIUM_CENTER,
        HIGH_CENTER,
        C_VARIANCE,
        VARIANCE,
        VARIANCE,
        VARIANCE,
        VARIANCE_OF_VARIANCE
    )


def gen_correct_solidity_params():
    LOW_CENTER = 0.427
    MEDIUM_CENTER = 0.566
    HIGH_CENTER = 0.751
    C_VARIANCE = 0.1
    VARIANCE = 0.2
    VARIANCE_OF_VARIANCE = 0.15
    return gen_correct_params(
        LOW_CENTER,
        MEDIUM_CENTER,
        HIGH_CENTER,
        C_VARIANCE,
        VARIANCE,
        VARIANCE,
        VARIANCE,
        VARIANCE_OF_VARIANCE
    )


def gen_correct_h_sym_params():
    LOW_CENTER = 0.345
    MEDIUM_CENTER = 0.486
    HIGH_CENTER = 0.621
    C_VARIANCE = 0.1
    VARIANCE = 0.2
    VARIANCE_OF_VARIANCE = 0.15
    return gen_correct_params(
        LOW_CENTER,
        MEDIUM_CENTER,
        HIGH_CENTER,
        C_VARIANCE,
        VARIANCE,
        VARIANCE,
        VARIANCE,
        VARIANCE_OF_VARIANCE
    )


def gen_correct_v_sym_params():
    LOW_CENTER = 0.333
    MEDIUM_CENTER = 0.468
    HIGH_CENTER = 0.615
    C_VARIANCE = 0.1
    VARIANCE = 0.2
    VARIANCE_OF_VARIANCE = 0.15
    return gen_correct_params(
        LOW_CENTER,
        MEDIUM_CENTER,
        HIGH_CENTER,
        C_VARIANCE,
        VARIANCE,
        VARIANCE,
        VARIANCE,
        VARIANCE_OF_VARIANCE
    )


def gen_random_params():
    MIN = 0
    MAX_CENTER = 2
    MAX_VARIANCE = 1
    while True:
        low_c = random.uniform(MIN, MAX_CENTER)
        low_v = random.uniform(MIN, MAX_VARIANCE)
        medium_c = low_c + random.uniform(MIN, MAX_CENTER)
        medium_v = random.uniform(MIN, MAX_VARIANCE)
        high_c = medium_c + random.uniform(MIN, MAX_CENTER)
        high_v = random.uniform(MIN, MAX_VARIANCE)
        if low_c < medium_c and medium_c < high_c:
            break
    return low_c, low_v, medium_c, medium_v, high_c, high_v


def gen_random_condition():
    return random.randint(-1, 2)


def gen_random_rule(number):
    rule = [gen_random_condition() for _ in range(7)]
    rule.append(number)
    return rule


def gen_random_rules():
    return [
        gen_random_rule(x) for x in range(10)
    ]


def gen_correct_rules():
    return [
        [-1, -1, -1, 2, -1, 2, 1, 0],
        [-1, 0, 2, -1, -1, 2, 0, 1],
        [1, -1, -1, 1, -1, -1, 0, 2],
        [-1, -1, -1, -1, 2, -1, 0, 3],
        [-1, -1, -1, 0, 0, 0, 1, 4],
        [1, -1, -1, 1, -1, -1, 0, 5],
        [0, -1, -1, -1, -1, -1, 1, 6],
        [2, 1, -1, -1, -1, -1, 0, 7],
        [-1, -1, -1, -1, -1, -1, 2, 8],
        [2, -1, -1, -1, -1, -1, 1, 9]
    ]