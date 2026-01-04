from bitalg.Projekt.utils.classes.Point import Point
from bitalg.Projekt.utils.classes.Triangle import Triangle
from bitalg.visualizer.main import Visualizer
from bitalg.Projekt.utils.orient import orient

def is_point_in_triangle(point: Point, triangle: Triangle) -> bool:
    p1, p2, p3 = triangle.get_points()
    o1 = orient(p1, p2, point)
    o2 = orient(p2, p3, point)
    o3 = orient(p3, p1, point)
    
    if (o1 >= 0 and o2 >= 0 and o3 >= 0) or (o1 <= 0 and o2 <= 0 and o3 <= 0):
        return True
    return False

def dfs_trianglation(point: Point, root: Triangle, vis: Visualizer = None) -> Triangle:
    if root.children == set():
        return root
    for child in root.children:
        if is_point_in_triangle(point, child):
            return dfs_trianglation(point, child, vis)
        else:
            pass
