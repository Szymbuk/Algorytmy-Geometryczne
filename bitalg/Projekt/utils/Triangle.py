from __future__ import annotations
import math
from bitalg.Projekt.utils.Point import Point
from bitalg.Projekt.utils.Section import Section
import numpy as np


from bitalg.Projekt.utils.orient import orient


class Triangle:

    def __init__(self, p1: Point | Section, p2: Point | Section, p3: Point | Section):
        self.__points: list['Point'] = []
        self.__edges: set['Section'] = set()

        if isinstance(p1,Point) and isinstance(p2,Point) and isinstance(p3,Point):
            self.__points.append(p1)
            self.__points.append(p2)
            self.__points.append(p3)

            # dodajemy krawędzie, jeżeli istniały to nie powinny się dublować
            s1,s2,s3 = Section(p1,p2),Section(p2,p3),Section(p3,p1)
            p1.add_edge(s1)
            p1.add_edge(s3)
            p2.add_edge(s1)
            p2.add_edge(s2)
            p3.add_edge(s2)
            p3.add_edge(s3)


            for edge in p1.get_edges():
                if p2 in edge.get_ends() or p3 in edge.get_ends():
                    edge.add_triangle(self)
                    self.__edges.add(edge)


            for edge in p2.get_edges():
                if p3 in edge.get_ends():
                    edge.add_triangle(self)
                    self.__edges.add(edge)





        elif isinstance(p1,Section) and isinstance(p2,Section) and isinstance(p3,Section):
            self.__edges.add(p1)
            self.__edges.add(p2)
            self.__edges.add(p3)

            # skoro istnieją odcinki to nie trzeba dodawać odcinków do punktów, bo te już tam są


            point1,point2 = p1.get_tuple_ends()
            point3, point4 = p2.get_tuple_ends()
            self.__points.append(point1)
            self.__points.append(point2)
            if point3 not in self.__points:
                self.__points.append(point3)
            else:
                self.__points.append(point4)

            p1.add_triangle(self)
            p2.add_triangle(self)
            p3.add_triangle(self)

        else:
            raise TypeError("Należy podać 3 punkty lub 3 odcinki")


        if orient(self.__points[0],self.__points[1],self.__points[2]) < 0:
            # gwarantuje odpowiednią kolejność wierzchołków (odwrotnie do ruchu wskazówek zegara)
            self.__points[1],self.__points[2] = self.__points[2],self.__points[1]


    def get_points(self) -> list[Point]:
        return self.__points

    def get_list_points(self):
        res = []
        for  x in list(self.__points):
            res.append(x.get_cords())
        return res

    def get_edges(self) -> set[Section]:
        return self.__edges

    def get_list_edges(self):
        res = []
        for x in list(self.__edges):
            res.append(x.get_tuple_ends())
        return res


    def define_circle(self) -> (Point, float):
        # korzystając z równania okręgu x^2 + y^2 + Dx + Ey + F = 0

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






