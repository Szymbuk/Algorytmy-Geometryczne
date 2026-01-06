from __future__ import annotations

from bitalg.Projekt.utils.classes.Point import Point, EPSILON
from bitalg.Projekt.utils.classes.Section import Section

from bitalg.Projekt.utils.find_sec_from_points import find_sec_from_points
from bitalg.Projekt.utils.orient import orient
from bitalg.visualizer.main import Visualizer

import math
import numpy as np


class Triangle:

    def __init__(self, obj1: Point | Section, obj2: Point | Section, obj3: Point | Section, build_graph: bool=False, vis_polygon = None):
        self.__points: list['Point'] = []
        self.__edges: set['Section'] = set()
        self.__vis_polygon = vis_polygon

        if build_graph:
            self.children: set['Triangle'] = set()

        objects = [obj1, obj2, obj3]

        if all(isinstance(obj, Point) for obj in objects):
            self.new_points(tuple(objects))

        elif all(isinstance(obj, Section) for obj in objects):
            for edge in objects:
                self.__edges.add(edge)

            points = obj1.get_ends() | obj2.get_ends()
            for point in points:
                self.__points.append(point)

            for obj in objects:
                obj.add_triangle(self)

        else:
            raise TypeError("Należy podać 3 punkty lub 3 odcinki.\n Podano {},{},{}".format(obj1.__class__.__name__,
                                                                                            obj2.__class__.__name__,
                                                                                            obj3.__class__.__name__))
        if abs(orient(self.__points[0],self.__points[1],self.__points[2]))<EPSILON:
            raise ValueError("Próba utworzenia trójkąta z punktów współliniowych")

        if orient(self.__points[0],self.__points[1],self.__points[2]) < 0:
            # gwarantuje odpowiednią kolejność wierzchołków (odwrotnie do ruchu wskazówek zegara)
            self.__points[1],self.__points[2] = self.__points[2],self.__points[1]

    def new_points(self, points: tuple[Point, Point, Point]) -> None:
        """
        Przypisuje nowe punkty oraz krawędzie danemu trójkątowi
        """
        self.__points = list(points)
        self.__edges = set()

        p1, p2, p3 = points

        # dodajemy krawędzie, jeżeli istniały to nie powinny się dublować
        new_sections_points = [(p1, p2), (p2, p3), (p3, p1)]
        new_sections = []
        for points in new_sections_points:
            sec = find_sec_from_points(points)
            new_sections.append(sec if sec else Section(*points))

        for section in new_sections:
            section.add_triangle(self)
            self.__edges.add(section)

        if orient(self.__points[0],self.__points[1],self.__points[2]) < 0:
            # gwarantuje odpowiednią kolejność wierzchołków (odwrotnie do ruchu wskazówek zegara)
            self.__points[1],self.__points[2] = self.__points[2],self.__points[1]  

    def get_points(self) -> list[Point]:
        return self.__points

    def get_list_tuple_points(self) -> list[tuple[int,int]]:
        """
        Zwraca listę punktów w postaci krotek ich współrzędnych
        """
        res = []
        for x in list(self.__points):
            res.append(x.get_cords())
        return res

    def get_edges(self) -> set[Section]:
        return self.__edges

    def get_list_edges(self) -> list[tuple[float, float]]:
        res = []
        for x in list(self.__edges):
            res.append(x.get_tuple_ends())
        return res

    def define_circle(self) -> tuple[Point, float]:
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
        try:
            x = np.linalg.solve(A,b)
        except np.linalg.LinAlgError:
            # Punkty współliniowe - okrąg ma nieskończony promień.
            # Zwracamy "bezpieczną" wartość, punkt bardzo daleko
            return Point(float('inf'), float('inf')), float('inf')


        D,E,F = x

        x0 = -D/2
        y0 = -E/2

        r = math.sqrt(x0**2 + y0**2 - F)

        return Point(x0,y0),r

    def destroy(self, vis: Visualizer = None):
        """
        Usuwa referencje z powiązanych krawędzi do danego trójkąta,
        jeżeli podano obiekt sceny, obiekt jest z niej usuwany
        """
        if vis is not None:
            if self.__vis_polygon is None:
                raise ValueError("Próba usunięcia ze sceny obiektu, który nie posiada referencji do obiektu sceny")
            vis.remove_figure(self.__vis_polygon)
        for edge in self.__edges:
            edge.remove_triangle(self)

    def set_vis_polygon(self, vis_polygon):
        """
        Przypisuje referencję do obiektu sceny
        """
        self.__vis_polygon = vis_polygon   

    def  __repr__(self) -> str:
        temp = self.get_list_edges()
        res = "Triangle: "
        for edge in temp:
            res += f"["
            for point in edge:
                res += f"({round(point[0], 2)}, {round(point[1], 2)})"
            res += "]  "
        res += "\n"
        return res






