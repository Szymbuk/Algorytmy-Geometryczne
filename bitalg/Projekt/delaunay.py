
from bitalg.Projekt.utils.classes.Point import Point
from bitalg.Projekt.utils.classes.Section import Section
from bitalg.Projekt.utils.classes.Triangle import Triangle

from utils.initial_triangle import get_initial_triangle


def triangulate(points: list[Point]) -> list[Triangle]:
    """
    Dla danego zbioru punktów zwraca triangulację Delaunaya tego zbioru
    """
    T = [get_initial_triangle(points)]
    n = len(points)

    for r in range(n):
        pass

    #
    # niedokończone
    #

    return T