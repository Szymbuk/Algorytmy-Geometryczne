from typing import List
from Projekt.utils.triangle_operations.orient import orient
from bitalg.visualizer.main import Visualizer
from Projekt.utils.custom_types import Point, PointIndex, PointsArray, TriangleIndex,EdgeAdjacencyMap, Triangle, EPSILON

def jump_and_walk_triangle_search(point_id: PointIndex, points_array: PointsArray, adjacency_graph: EdgeAdjacencyMap, triangles: List[Triangle], vis: Visualizer| None = None) -> TriangleIndex:
    return jump_and_walk_point_search(points_array[point_id], points_array, adjacency_graph, triangles, vis)[0]


def jump_and_walk_point_search(point: Point, points_array: PointsArray, adjacency_graph: EdgeAdjacencyMap, triangles: List[Triangle], vis: Visualizer| None = None) -> tuple[TriangleIndex, list[TriangleIndex]]:
    actual_triangle_id = next(
        triangle_id
        for triangle_ids in adjacency_graph.values()
        for triangle_id in triangle_ids
    )
    visited = [actual_triangle_id]
    # Zabezpieczenie przed pętlą nieskończoną
    steps = 0
    max_steps = len({
        triangle_id
        for triangle_ids in adjacency_graph.values()
        for triangle_id in triangle_ids
    }) + 1

    while steps <= max_steps:
        next_triangle_id = jump_and_walk_next_point(point, actual_triangle_id, points_array, adjacency_graph, triangles)
        
        if next_triangle_id == actual_triangle_id:
            return actual_triangle_id, visited
        actual_triangle_id = next_triangle_id
        visited.append(actual_triangle_id)
        steps+=1

    raise RuntimeError("Punkt poza granicami triangulacji")

def jump_and_walk_next(point_id: PointIndex, triangle_id: TriangleIndex, points: PointsArray, adjacency_graph: EdgeAdjacencyMap,triangles: List[Triangle]) -> TriangleIndex:
    return jump_and_walk_next_point(points[point_id], triangle_id, points, adjacency_graph, triangles)


def jump_and_walk_next_point(point: Point, triangle_id: TriangleIndex, points: PointsArray, adjacency_graph: EdgeAdjacencyMap,triangles: List[Triangle]) -> TriangleIndex:
    p1_ind, p2_ind, p3_ind = triangles[triangle_id]
    pairs = [(p1_ind, p2_ind), (p2_ind, p3_ind), (p3_ind, p1_ind)]
    for a, b in pairs:
        det = orient((points[a], points[b], point))
        if a>b:
            a,b = b,a
        if det < -EPSILON:
            # Znaleziono krawędź, dla której punkt jest po prawej stronie, wychodzimy przez nią z trójkąta
            candidates_id= adjacency_graph[(a, b)]
            for candidate_id in candidates_id:
                if candidate_id != triangle_id:
                    return candidate_id

    return triangle_id
