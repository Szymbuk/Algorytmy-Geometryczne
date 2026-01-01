from bitalg.Projekt.utils.classes.Point import Point
from typing import TYPE_CHECKING

import itertools


if TYPE_CHECKING:
    from bitalg.Projekt.utils.classes.Triangle import Triangle


class Section:

    id_iter = itertools.count(start=0)

    def __init__(self, p1: Point, p2: Point):
        self.__ends = set()
        self.__ends.add(p1)
        self.__ends.add(p2)
        self.__id = next(self.id_iter)
        self.__triangles = set()
        p1.add_edge(self)
        p2.add_edge(self)

    def add_triangle(self, triangle: 'Triangle'):
        self.__triangles.add(triangle)
        if len(self.__triangles) >2:
            raise ValueError("Only 2 triangles can be assigned to a single Section object")


    def get_ends(self) -> set[Point]:
        return self.__ends

    def get_tuple_ends(self):
        res = []
        for x in list(self.__ends):
            res.append(x.get_cords())
        return res

    def get_triangles(self) -> set['Triangle']:
        return self.__triangles

    def get_id(self) -> int:
        return self.__id

    def on_section(self,point:Point):
        return point.on_section(self)

    def  __repr__(self) -> str:
        return "Section: ({})".format(self.get_tuple_ends())

    def __eq__(self, other: 'Section'):
        if self.get_id() == other.get_id(): return True
        p1, p2 = self.get_tuple_ends()
        p3, p4 = other.get_tuple_ends()
        return (p1==p3 and p2==p4) or (p1==p4 and p2==p3)

    def __hash__(self):
        return hash(self.get_tuple_ends()[0]) + hash(self.get_tuple_ends()[1])


