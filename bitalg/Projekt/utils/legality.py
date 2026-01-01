from bitalg.Projekt.utils.classes.Point import Point
from bitalg.Projekt.utils.classes.Section import Section
from bitalg.Projekt.utils.classes.Triangle import Triangle

def turned_points(sec: Section) -> tuple[Point, Point, Point, Point]:
    """
    Zwraca punkty, które byłyby końcami odcinka po jego przekręceniu
    """
    t1, t2 = tuple(sec.get_triangles())
    edges = t1.get_edges() | t2.get_edges()
    points = set()
    for edge in edges:
        points |= edge.get_ends()

    new_sec_pts = points.difference(sec.get_ends())
    
    return new_sec_pts

def turn(sec: Section) -> tuple[Point, Point]:
    """
    Dokonuje "przekręcenia" krawędzi w triangulacji
    """
    t1, t2 = tuple(sec.get_triangles())
    sec_pts = sec.get_ends()
    new_sec_pts = turned_points(sec)

    p1, p2 = tuple(sec_pts)
    p3, p4 = tuple(new_sec_pts)

    t1.new_points((p1, p3, p4))
    t2.new_points((p2, p3, p4))

    return p3, p4

def is_legal(sec: Section):
    t1, t2 = tuple(sec.get_triangles())
    
    new_sec_pts = turned_points(sec)
    p1, p2 = tuple(new_sec_pts)

    center, radius = t1.define_circle()
    point = p2 if p1 in t1.get_points() else p1
    
    return not point.in_circle(center, radius)

def legalize_edge():
    pass
