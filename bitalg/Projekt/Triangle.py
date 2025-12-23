import math


from bitalg.Projekt.Point import Point
from bitalg.Projekt.Section import Section
import numpy as np


class Triangle:
    def __init__(self, p1: Point | Section, p2: Point | Section, p3: Point | Section):
        self.__points = set()
        self.__edges = set()

        if isinstance(p1,Point) and isinstance(p2,Point) and isinstance(p3,Point):
            self.__points.add(p1)
            self.__points.add(p2)
            self.__points.add(p3)
            for edge in p1.get_edges():
                if p2 in edge.get_ends() or p3 in edge.get_ends():
                    self.__edges.add(edge)


            for edge in p2.get_edges():
                if p3 in edge.get_ends():
                    self.__edges.add(edge)




        elif isinstance(p1,Section) and isinstance(p2,Section) and isinstance(p3,Section):
            self.__edges.add(p1)
            self.__edges.add(p2)
            self.__edges.add(p3)

            self.__points.add(p1.get_ends())
            self.__points.add(p2.get_ends())

        else:
            raise TypeError("Należy podać 3 punkty lub 3 odcinki")

    def get_points(self) -> set[Point]:
        return self.__points

    def get_edges(self) -> set[Section]:
        return self.__edges

    def get_list_edges(self):
        res = []
        for x in list(self.__edges):
            res.append(x.get_tuple_ends())
        return res


    def define_circle(self) -> (Point, float):
        # korzystając z rówania okręgu x^2 + y^2 + Dx + Ey + F = 0

        p1,p2,p3 = self.__points
        A = np.array([[p1.get_x(),p1.get_y(),1],
                     [p2.get_x(), p2.get_y(), 1],
                     [p3.get_x(), p3.get_y(), 1]
                      ])
        b = np.array([-(p1.get_x()**2 + p1.get_y()**2),
                     -(p2.get_x() ** 2 + p2.get_y() ** 2),
                     -(p3.get_x() ** 2 + p3.get_y() ** 2),
                     ])
        x = np.linalg.solve(A,b)


        D,E,F = x
        print(D,E,F)

        x0 = -D/2
        y0 = -E/2

        r = math.sqrt(x0**2 + y0**2 - F)

        return Point(x0,y0, -10),r

    def  __repr__(self) -> str:
        temp = self.get_list_edges()
        res = "Triangle:\n"
        for i in temp:
            res += "{}\n".format(i)
        res += "\n"
        return res






