from bitalg.Projekt.utils.classes.Point import Point
from bitalg.Projekt.utils.classes.Section import Section
from bitalg.Projekt.utils.classes.Triangle import Triangle

from typing import Literal
from bitalg.Projekt.utils.jump_and_walk import jump_and_walk_triangle_search
from bitalg.visualizer.main import Visualizer


def find_triangle_containing_point(point: Point, T: list[Triangle], variant: Literal["JaW", "ten drugi algorytm"],vis: Visualizer = None) -> Triangle:
    """
    Zwraca trójkąt triangulacji który zawiera dany punkt, możliwe są dwa warianty 
    czyli dwa różne algorytmy znajdowania tego punktu:
    "JaW" - Jump and Walk
    "..." - ten drugi co go jeszcze nie ma
    """
    if variant == "JaW":
        return jump_and_walk_triangle_search(point, T,vis)
    else:
        #
        # niedokończone
        #
        pass

def find_sec_in_T(points: tuple[Point, Point]) -> Section:
    """
    Znajduje odcinek w triangulacji
    """

    """
    sec = Section(points[0], points[1])
    sections = set()
    for trian in T:
        sections |= trian.get_edges()

    for section in sections:
        if sec == section: return section
    raise LookupError("Odcinek nie należy do triangulacji")
    """
    p1,p2 = points
    for edge in p1.get_edges():
        if p2 in edge.get_ends():
            return edge
    raise LookupError("Odcinek nie należy do triangulacji")

