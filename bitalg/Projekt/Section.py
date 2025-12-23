from bitalg.Projekt.Point import Point


class Section:
    def __init__(self, p1: Point, p2: Point, section_id: int):
        self.__ends = set()
        self.__ends.add(p1)
        self.__ends.add(p2)
        self.__id = section_id
        p1.add_edge(self)
        p2.add_edge(self)

    def get_ends(self) -> set[Point]:
        return self.__ends

    def get_tuple_ends(self):
        res = []
        for x in list(self.__ends):
            res.append(x.get_cords())
        return res

    def get_id(self) -> int:
        return self.__id

    def  __repr__(self) -> str:
        return "Section: ({})".format(self.get_tuple_ends())


