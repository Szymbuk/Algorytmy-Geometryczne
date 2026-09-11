import numpy as np

from Projekt.utils.custom_types import PointIndex, Triangle, TriangleIndex
from Projekt.utils.triangle_search.search_triangulation import (
    find_triangle_containing_point,
)


def test_jump_and_walk_finds_point_in_single_triangle():
    points = np.array([[0.0, 0.0], [2.0, 0.0], [0.0, 2.0], [0.5, 0.5]])
    triangle: Triangle = (PointIndex(0), PointIndex(1), PointIndex(2))
    adjacency_graph = {
        (PointIndex(0), PointIndex(1)): [TriangleIndex(0)],
        (PointIndex(0), PointIndex(2)): [TriangleIndex(0)],
        (PointIndex(1), PointIndex(2)): [TriangleIndex(0)],
    }

    result = find_triangle_containing_point(
        PointIndex(3),
        "JaW",
        points,
        adjacency_graph,
        [triangle],
        [set()],
    )

    assert result == TriangleIndex(0)
