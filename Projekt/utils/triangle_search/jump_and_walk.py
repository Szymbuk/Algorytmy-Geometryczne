from typing import List
from Projekt.utils.triangle_operations.orient import orient
from bitalg.visualizer.main import Visualizer
from Projekt.utils.custom_types import PointIndex, PointsArray, TriangleIndex,EdgeAdjacencyMap, Triangle, EPSILON

def jump_and_walk_triangle_search(point_id: PointIndex, points_array: PointsArray, adjacency_graph: EdgeAdjacencyMap, triangles: List[Triangle], vis: Visualizer| None = None) -> TriangleIndex:
    actual_triangle_id = TriangleIndex(len(triangles) - 1)
    # Zabezpieczenie przed pętlą nieskończoną
    steps = 0
    max_steps = len(adjacency_graph)   + 1# Pesymistycznie nie powinniśmy odwiedzić więcej niż N trójkątów

    while steps <= max_steps:
        next_triangle_id = jump_and_walk_next(point_id, actual_triangle_id, points_array, adjacency_graph, triangles)
        
        if next_triangle_id == actual_triangle_id:
            return actual_triangle_id
        actual_triangle_id = next_triangle_id
        steps+=1

    print("Warning: Jump-and-Walk failed, switching to brute-force.")
    for t_ind in [t for triangles in adjacency_graph.values() for t in triangles]:
        point = points_array[point_id]
        p1, p2, p3 = points_array[list(triangles[t_ind])]
        if (orient((p1, p2, point)) >= -EPSILON and
                orient((p2, p3, point)) >= -EPSILON and
                orient((p3, p1, point)) >= -EPSILON):
            return t_ind
    raise RuntimeError("Punkt poza granicami triangulacji")

def jump_and_walk_next(point_id: PointIndex, triangle_id: TriangleIndex, points: PointsArray, adjacency_graph: EdgeAdjacencyMap,triangles: List[Triangle]) -> TriangleIndex:
    p1_ind, p2_ind, p3_ind = triangles[triangle_id]
    pairs = [(p1_ind, p2_ind), (p2_ind, p3_ind), (p3_ind, p1_ind)]
    for a, b in pairs:
        if a>b:
            a,b = b,a
        det = orient((points[a], points[b], points[point_id]))
        if det < -EPSILON:
            # Znaleziono krawędź, dla której punkt jest po prawej stronie, wychodzimy przez nią z trójkąta
            candidates_id= adjacency_graph[(a, b)]
            for candidate_id in candidates_id:
                if candidate_id != triangle_id:
                    return candidate_id

    return triangle_id
