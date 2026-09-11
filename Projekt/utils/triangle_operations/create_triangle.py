

from Projekt.utils.custom_types import PointIndex, PointsArray, Triangle, EPSILON
from Projekt.utils.triangle_operations.orient import orient


def make_ccw_triangle(
    p1: PointIndex,
    p2: PointIndex,
    p3: PointIndex,
    points: PointsArray,
) -> Triangle:
    orientation = orient((
        points[p1],
        points[p2],
        points[p3],
    ))

    if orientation > EPSILON:
        return p1, p2, p3

    if orientation < -EPSILON:
        return p1, p3, p2

    raise RuntimeError("Trójkąt jest zdegenerowany.")