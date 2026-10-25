
from typing import List
import numpy as np
from Projekt.utils.custom_types import PointsArray, TriangleIndex, Triangle, Point, PointIndex
from bitalg.visualizer.main import Visualizer
from Projekt.utils.triangle_operations.orient import orient

def is_point_in_triangle(point: Point, triangle: Triangle, points: PointsArray) -> bool:
    p1_ind, p2_ind, p3_ind = triangle
    p1,p2,p3 = points[p1_ind], points[p2_ind], points[p3_ind]
    
    o1 = orient((p1, p2, point))
    o2 = orient((p2, p3, point))
    o3 = orient((p3, p1, point))
    
    if (o1 >= 0 and o2 >= 0 and o3 >= 0) or (o1 <= 0 and o2 <= 0 and o3 <= 0):
        return True
    return False

def dfs_trianglation(point_id: PointIndex, root_id: TriangleIndex, triangles: List[Triangle], child_graph: list[set[TriangleIndex]],points: PointsArray, vis: Visualizer| None = None) -> TriangleIndex:
    return dfs_trianglation_point(points[point_id], root_id, triangles, child_graph, points, vis)[0]


def dfs_trianglation_point(point: Point, root_id: TriangleIndex, triangles: List[Triangle], child_graph: list[set[TriangleIndex]], points: PointsArray, vis: Visualizer| None = None) -> tuple[TriangleIndex, list[TriangleIndex]]:
    visited = [root_id]

    def search(triangle_id: TriangleIndex) -> TriangleIndex:
        if child_graph[triangle_id] == set():
            return triangle_id
        for child in child_graph[triangle_id]:
            if is_point_in_triangle(point, triangles[child], points):
                visited.append(child)
                return search(child)
        raise RuntimeError(f"Punkt {point} poza granicami triangulacji.")

    return search(root_id), visited