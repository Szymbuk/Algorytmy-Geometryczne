import numpy as np
from Projekt.utils.custom_types import PointIndex, TriangleIndex, EPSILON
from Projekt.utils.triangle_operations.legality import turned_points



def test_turned_points_returns_correct_points():
    adjacency_graph = {
        (PointIndex(0), PointIndex(1)): (TriangleIndex(0), TriangleIndex(1)),
        (PointIndex(0), PointIndex(2)): (TriangleIndex(0), TriangleIndex(2)),
        (PointIndex(1), PointIndex(2)): (TriangleIndex(1), TriangleIndex(2)),
    }

    p1, p2 = PointIndex(0), PointIndex(1)
    expected_points = (PointIndex(2), PointIndex(3))

    result = turned_points(p1, p2, adjacency_graph)

    assert result == expected_points