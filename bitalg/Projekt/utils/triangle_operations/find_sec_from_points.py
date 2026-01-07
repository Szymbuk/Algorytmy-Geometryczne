from bitalg.Projekt.utils.classes.Point import Point
from bitalg.Projekt.utils.classes.Section import Section

from typing import Union

def find_sec_from_points(points: tuple[Point, Point]) -> Union[bool, Section]:
    """
    Zwraca odcinek o końcach w podanych punktach, jeżeli taki nie istnieje zwraca False
    """
    p1,p2 = points
    for edge in p1.get_edges():
        if p2 in edge.get_ends():
            return edge
    return False