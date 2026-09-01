import numpy as np


def generate_uniform_points(left=-100, right=100, n=100) -> np.array:
    return np.random.uniform(left,right,2*n).reshape(n,2)