
from bitalg.Projekt.utils.classes.Point import Point
from bitalg.Projekt.utils.classes.Section import Section
from bitalg.Projekt.utils.classes.Triangle import Triangle

from utils.initial_triangle import get_initial_triangle
from utils.search_triangulation import find_triangle_containg_point


def triangulate(p: list[Point]) -> list[Triangle]:
    """
    Dla danego zbioru punktów zwraca triangulację Delaunaya tego zbioru
    """
    T = [get_initial_triangle(p)]
    n = len(p)

    for r in range(n):
        triangle = find_triangle_containg_point(p[r], T, variant="JaW")
        print(T[0] == triangle)
        break


    #
    # niedokończone
    #

    return T