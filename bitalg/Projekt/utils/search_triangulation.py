from bitalg.Projekt.utils.classes.Point import Point
from bitalg.Projekt.utils.classes.Section import Section
from bitalg.Projekt.utils.classes.Triangle import Triangle

from typing import Literal
from utils.jump_and_walk import jump_and_walk_triangle_search

def find_triangle_containg_point(point: Point, T: list[Triangle], variant: Literal["JaW", "ten drugi algorytm"]) -> Triangle:
    if variant == "JaW":
        return jump_and_walk_triangle_search(point, T)
    else:
        #
        # niedokończone
        #
        pass

def find_sec_in_T(points: tuple[Point, Point], T: list[Triangle]) -> Section:
    """
    Znajduje odcinek w triangulacji
    """
    sec = Section(points[0], points[1])
    sections = set()
    for trian in T:
        sections |= trian.get_edges()

    for section in sections:
        if sec == section: return section
    raise LookupError("Odcinek nie należy do triangulacji")
