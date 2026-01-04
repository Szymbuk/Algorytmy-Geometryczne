from bitalg.Projekt.utils.classes.Point import Point
from bitalg.Projekt.utils.classes.Triangle import Triangle
from bitalg.Projekt.utils.orient import orient
from bitalg.visualizer.main import Visualizer


def jump_and_walk_triangle_search(point: Point, triangles: list[Triangle], vis: Visualizer = None) -> Triangle:
    actual_triangle = triangles[0]
    while True:
        next_triangle = jump_and_walk_next(point, actual_triangle)
        if next_triangle == actual_triangle:
            return actual_triangle
        actual_triangle = next_triangle

def jump_and_walk_next(point: Point, triangle:Triangle) -> Triangle:
    p1, p2, p3 = triangle.get_points()
    pairs = [(p1, p2), (p2, p3), (p3, p1)]

    edge = None
    for a, b in pairs:
        det = orient(a, b, point)
        if det < 0:
            edges = list(a.get_edges())
            for sample_edge in edges:
                edge = sample_edge if b in sample_edge.get_ends() else edge
            break 
    else:
        return triangle 

    try:
        t1, t2 = list(edge.get_triangles())
        return t1 if triangle == t2 else t2
    except ValueError: # w wypadku gdy jest tylko jeden sąsiadujący trójkąt
        return triangle
