from typing import List

from Projekt.utils.classes.Triangle import Triangle
from Projekt.utils.triangle_operations.orient import orient
from bitalg.visualizer.main import Visualizer
from Projekt.utils.classes.Triangle import EPSILON
from Projekt.utils.custom_types import PointIndex,PointsArray


def jump_and_walk_triangle_search(point_id: PointIndex, points_array: PointsArray, adjacency_graph: dict[tuple[PointIndex, PointIndex],List[Triangle]], vis: Visualizer = None) -> Triangle:
    if not hasattr(jump_and_walk_triangle_search, "last_triangle"):
        jump_and_walk_triangle_search.last_triangle = None

    # Próbujemy użyć ostatniego trójkąta jako startowego
    actual_triangle = jump_and_walk_triangle_search.last_triangle

    if actual_triangle is None or actual_triangle not in [t for triangles in adjacency_graph.values() for t in triangles]:
        actual_triangle = next(iter(adjacency_graph.values()))[0]
    # Zabezpieczenie przed pętlą nieskończoną
    steps = 0
    max_steps = len(adjacency_graph)   + 1# Pesymistycznie nie powinniśmy odwiedzić więcej niż N trójkątów

    while steps <= max_steps:
        next_triangle = jump_and_walk_next(point_id, actual_triangle, points_array, adjacency_graph)
        if next_triangle == actual_triangle:
            jump_and_walk_triangle_search.last_triangle = actual_triangle
            return actual_triangle
        actual_triangle = next_triangle
        steps+=1

    print("Warning: Jump-and-Walk failed, switching to brute-force.")
    jump_and_walk_triangle_search.last_triangle = None
    for t in [t for triangles in adjacency_graph.values() for t in triangles]:
        point = points_array[point_id]
        p1, p2, p3 = points_array[list(t.get_points())]
        if (orient((p1, p2, point)) >= -EPSILON and
                orient((p2, p3, point)) >= -EPSILON and
                orient((p3, p1, point)) >= -EPSILON):
            return t
    raise ValueError("Punkt poza granicami triangulacji")

def jump_and_walk_next(point_id: PointIndex, triangle: Triangle, points: PointsArray, adjacency_graph: dict[tuple[PointIndex, PointIndex], List[Triangle]]) -> Triangle:
    p1_ind, p2_ind, p3_ind = triangle.get_points()
    pairs = [(p1_ind, p2_ind), (p2_ind, p3_ind), (p3_ind, p1_ind)]
    for a, b in pairs:
        det = orient((points[a], points[b], points[point_id]))
        if det < -EPSILON:
            # Znaleziono krawędź, dla której punkt jest po prawej stronie, wychodzimy przez nią z trójkąta
            candidates= adjacency_graph[tuple(sorted((a, b)))]
            print(candidates)
            for candidate_triangle in candidates:
                if candidate_triangle != triangle:
                    return candidate_triangle

    return triangle
