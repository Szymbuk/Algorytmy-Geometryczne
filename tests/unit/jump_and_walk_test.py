from Projekt.utils.triangle_search.jump_and_walk import jump_and_walk_next
from Projekt.utils.custom_types import EdgeAdjacencyMap, PointIndex, PointsArray, Triangle, TriangleIndex
import numpy as np


def test_jump_and_walk_next_moves_to_triangle_across_edge():
    p0 = np.array([0, 0])
    p1 = np.array([6, 0])
    p2 = np.array([3, 1])
    p3 = np.array([8, 1])
    p4 = np.array([0, 4])
    p5 = np.array([2, 6])
    p6 = np.array([1, 8])
    p7 = np.array([6, 10])
    p8 = np.array([8, 12])
    p9 = np.array([7, 18])
    p10 = np.array([4, 4])
    px = np.array([7, 12])

    points: PointsArray = np.array([p0, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, px])

    triangles: list[Triangle] = [
        (PointIndex(1), PointIndex(10), PointIndex(2)),
        (PointIndex(1), PointIndex(3), PointIndex(7)),
        (PointIndex(1), PointIndex(7), PointIndex(10)),
        (PointIndex(2), PointIndex(10), PointIndex(5)),
        (PointIndex(2), PointIndex(5), PointIndex(4)),
        (PointIndex(4), PointIndex(5), PointIndex(6)),
        (PointIndex(5), PointIndex(7), PointIndex(6)),
        (PointIndex(10), PointIndex(7), PointIndex(5)),
        (PointIndex(3), PointIndex(8), PointIndex(7)),
        (PointIndex(7), PointIndex(8), PointIndex(9)),
        (PointIndex(7), PointIndex(9), PointIndex(6)),
    ]

    adjacency_graph: EdgeAdjacencyMap = {}
    for triangle_id, triangle in enumerate(triangles):
        p1, p2, p3 = triangle
        for px,py in ((p1, p2), (p2, p3), (p3, p1)):
            if px>py:
                px,py = py,px
            edge = (px, py)
            adjacency_graph.setdefault(edge, []).append(TriangleIndex(triangle_id))

    result = jump_and_walk_next(
        PointIndex(11),
        TriangleIndex(4),
        points,
        adjacency_graph,
        triangles,
    )

    assert result == TriangleIndex(3)