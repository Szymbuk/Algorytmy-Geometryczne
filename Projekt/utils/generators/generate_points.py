import numpy as np
from Projekt.utils.custom_types import PointsArray

def generate_uniform_points(left=-100, right=100, n=100) -> PointsArray:
    return np.random.uniform(left,right,2*n).reshape(n,2)