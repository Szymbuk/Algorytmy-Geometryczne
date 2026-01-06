import math
from typing import TYPE_CHECKING
import itertools

from bitalg.Projekt.utils.orient import orient

if TYPE_CHECKING:
    from bitalg.Projekt.utils.classes.Section import Section
    from bitalg.Projekt.utils.classes.Triangle import Triangle

EPSILON = 10e-12

class Point:

    id_iter = itertools.count(start=1)

    def __init__(self, x: float, y: float):
        self.__x= x
        self.__y = y
        self.__id = next(self.id_iter)
        self.__edges: set['Section'] = set()

    def get_x(self) -> float:
        return self.__x

    def get_y(self) -> float:
        return self.__y

    def get_cords(self) -> tuple[float,float]:
        return self.__x, self.__y

    def get_id(self) -> int:
        return self.__id

    def get_edges(self) -> set['Section']:
        return self.__edges

    def add_edge(self, section:'Section') -> None:
        self.__edges.add(section)

    def remove_edge(self, section:'Section') -> None:
        self.__edges.remove(section)

    def in_circle(self, point: 'Point', r: float) -> bool:
        return math.sqrt((self.__x-point.get_x())**2 + (self.__y-point.get_y())**2 ) - r < -EPSILON

    def on_section(self, section: 'Section') -> bool:
        start,end = list(section.get_ends())

        return -EPSILON < orient(start,end,self)<EPSILON

    def __eq__(self, other: 'Point'):
        if self.__id == other.get_id(): return True
        return self.__x == other.get_x() and self.__y == other.get_y()

    def __hash__(self):
        return hash(self.__x) + hash(self.__y) + hash(self.__id)

    def  __repr__(self) -> str:
        return "Point({},{})".format(round(self.__x, 2), round(self.__y, 2))


