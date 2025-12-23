from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bitalg.Projekt.Section import Section


class Point:

    def __init__(self, x: float, y: float, point_id: int):
        self.__x= x
        self.__y = y
        self.__id = point_id
        self.__edges = set()

    def get_x(self) -> float:
        return self.__x

    def get_y(self) -> float:
        return self.__y

    def get_cords(self) -> (float,float):
        return self.__x, self.__y

    def get_id(self) -> int:
        return self.__id

    def get_edges(self) -> set['Section']:
        return self.__edges

    def add_edge(self,section:'Section') -> None:
        self.__edges.add(section)

    def  __repr__(self) -> str:
        return "Point: ({},{})".format(self.__x,self.__y)

