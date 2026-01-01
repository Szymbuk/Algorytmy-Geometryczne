from bitalg.Projekt.utils.classes.Point import Point
from bitalg.Projekt.utils.classes.Section import Section
from bitalg.Projekt.utils.classes.Triangle import Triangle

from utils.search_triangulation import find_sec_in_T

def turn(sec: Section):
    """
    Dokonuje "przekręcenia" krawędzi w triangulacji
    """

    t1, t2 = tuple(sec.get_triangles())
    edges = t1.get_edges() | t2.get_edges()
    points = set()
    for edge in edges:
        points |= edge.get_ends()

    sec_pts = sec.get_ends()
    new_sec_pts = points.difference(sec_pts)

    p1, p2 = tuple(sec_pts)
    p3, p4 = tuple(new_sec_pts)

    t1.new_points((p1, p3, p4))
    t2.new_points((p2, p3, p4))

    return p3, p4

def is_legal(sec: Section):
    pass

def legalize_edge():
    pass
