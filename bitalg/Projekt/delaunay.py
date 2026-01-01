
from bitalg.Projekt.utils.classes.Point import Point
from bitalg.Projekt.utils.classes.Section import Section
from bitalg.Projekt.utils.classes.Triangle import Triangle

from utils.orient import orient
from utils.initial_triangle import get_initial_triangle
from utils.search_triangulation import find_triangle_containing_point

def is_point_on_triangle_edge(p: Point, triangle: Triangle, eps = 1e-12) -> bool:
    a, b, c = triangle.get_points()

    d1 = orient(p, a, b)
    d2 = orient(p, b, c)
    d3 = orient(p, c, a)

    return abs(d1) < eps or abs(d2) < eps or abs(d3) < eps

def triangulate(p: list[Point]) -> list[Triangle]:
    """
    Dla danego zbioru punktów zwraca triangulację Delaunaya tego zbioru
    """
    T = [get_initial_triangle(p)]
    n = len(p)

    for r in range(n):
        triangle = find_triangle_containing_point(p[r], T, variant="JaW")
        
        if is_point_on_triangle_edge(p[r], triangle):
            pass
        else:
            pass

    #
    # niedokończone
    #

    return T