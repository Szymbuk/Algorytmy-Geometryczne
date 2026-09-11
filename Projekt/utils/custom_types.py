from jaxtyping import Float
from typing import NewType, Literal
from numpy import ndarray

Point = Float[ndarray, "2"]

PointsArray = Float[ndarray, "N 2"]
PointIndex = NewType("PointIndex", int)

Triangle = tuple[PointIndex, PointIndex, PointIndex]
TriangleIndex = NewType("TriangleIndex", int)

EdgeAdjacencyMap = dict[tuple[PointIndex,PointIndex],list[TriangleIndex]]

variants = Literal["JaW", "Graph"]
EPSILON = 1e-12