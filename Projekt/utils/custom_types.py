from jaxtyping import Float
from typing import NewType
from numpy import ndarray

Point = Float[ndarray, "2"]
PointsArray = Float[ndarray, "N 2"]

PointIndex = NewType("PointIndex", int)