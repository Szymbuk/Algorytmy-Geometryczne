
# from Projekt.utils.classes.Point import Point, EPSILON
# rom Projekt.utils.classes.Section import Section
from Projekt.utils.custom_types import Point, PointIndex, PointsArray, TriangleIndex
from Projekt.utils.Triangle import Triangle
from Projekt.utils.triangle_operations.legality import legalize_edge, turned_points

from Projekt.utils.triangle_operations.orient import orient
# from Projekt.utils.triangle_operations.find_sec_from_points import find_sec_from_points
from Projekt.utils.triangle_search.search_triangulation import find_triangle_containing_point
from bitalg.visualizer.main import Visualizer
from Projekt.utils.Triangle import  EPSILON

import numpy as np
from typing import Union, Literal, List
from numpy._typing import NDArray
from Projekt.utils.custom_types import EdgeAdjacencyMap




class Triangulation:
    def __init__(self, points: PointsArray, variant: Literal["JaW", "Graph"]="JaW", vis: Visualizer = None):
        self.__points = points
        self.__variant = variant
        self.__triangulation: set[TriangleIndex] = set({}) # set of triangle t_id's
        self.__adjacency_graph: EdgeAdjacencyMap = {}
        self.__vis = vis
        self.__triangles: list[Triangle] = [] # A list of all triangles created during the triangulation process, indexed by their t_id's.


    def is_point_on_triangle_edge(self,px: Point, triangle_id: TriangleIndex) -> Union[bool, tuple[PointIndex, PointIndex]]:
        """
        Przyjmuje punkt oraz trójkąt. Jeżeli punkt leży na którejś z krawędzi trójkąta, zwraca tę krawędź,
        w przeciwnym razie zwraca False.
        """
        a, b, c = self.__triangles[triangle_id].get_points()

        edges = [tuple(sorted((a, b))), tuple(sorted((b, c))), tuple(sorted((c, a)))]

        for edge in edges:
            p1,p2 = self.__points[list(edge)]
            det = orient((p1,p2,px))
            if abs(det) < EPSILON:
                if edge[0] < edge[1]:
                    return edge[0],edge[1]
                else:
                    return edge[1],edge[0]
        return False

    def triangulate(self) -> None:
        """
        Dla danego zbioru punktów zwraca triangulację Delaunaya tego zbioru
        Parametr variant odpowiada za wariant algorytmu wyszukiwania trójkąta, który zawiera zadany punkt
        """

        build_graph = True if self.__variant == "Graph" else False

        initial_triangle = self.get_initial_triangle(build_graph)
        self.__triangles.append(initial_triangle)

        t_id = initial_triangle.get_id()
        self.__triangulation.add(t_id)

        p1,p2,p3 = initial_triangle.get_points()
        for p_0,p_1 in [(p1,p2),(p2,p3),(p3,p1)]:
            self.__adjacency_graph[(p_0,p_1)] = [t_id]

        if self.__vis is not None:
            vis_initial_points = self.__vis.add_point(self.__points[list(initial_triangle.get_points())], color='orange')
            vis_initial_triangle = self.__vis.add_polygon(self.__points[list(initial_triangle.get_points())], color='green', fill=False)
            initial_triangle.set_vis_polygon(vis_initial_triangle)

        for point_ind, point in enumerate(self.__points):
            point: Point
            point_ind: PointIndex
            if self.__vis is not None:
                self.__vis.add_point(point, color="red")

            curr_triangle_id = find_triangle_containing_point(point_ind,self.__variant, initial_triangle,self.__points, self.__adjacency_graph,self.__triangles,  self.__vis)
            potential_edge = self.is_point_on_triangle_edge(point, curr_triangle_id)

            if potential_edge: # punkt na krawędzi trójkąta

                # removing from adjacency graph.
                t1, t2 = self.__adjacency_graph.pop(potential_edge)
                i, j = potential_edge
                k, l = turned_points(i, j, self.__adjacency_graph)

                # removing a vis object of triangle.
                self.__triangles[t1].destroy(self.__vis)
                self.__triangles[t2].destroy(self.__vis)

                # removing a triangle from the triangulation set.
                self.__triangulation.remove(t1)
                self.__triangulation.remove(t2)

                new_triangles: list[TriangleIndex] = []
                new_sections_points = [(i, k), (i, l), (j, k), (j, l)]
                for p1,p2 in new_sections_points:
                    pt1, pt2, pt3 = self.__points[[p1, p2, point_ind]]
                    det = orient((pt1, pt2, pt3))
                    new_id = TriangleIndex(len(self.__triangles))
                    if det < -EPSILON:
                        t = Triangle((point_ind,p2,p1),build_graph)
                    elif det > EPSILON:
                        t = Triangle((p1,p2,point_ind),build_graph)
                    else:
                        raise RuntimeError("Punkt jest współliniowy z krawędzią, co nie powinno się zdarzyć w tym miejscu.")


                    new_triangles.append(new_id)
                    self.__triangles.append(t)
                    self.__triangulation.add(new_id)

                    for px,py in [(p1,p2),(p2,point),(p1,point)]:
                        if px<py:
                            px,py = py,px
                        if (px,py) not in self.__adjacency_graph:
                            self.__adjacency_graph[px,py] = [new_id]
                        else:
                            self.__adjacency_graph[px,py].append(new_id)
                            if len(self.__adjacency_graph[px,py]) > 2:
                                raise RuntimeError(f"Niepoprawna liczba trójkątów w grafie sąsiedztwa dla krawędzi: {(px,py)}")

                if build_graph:
                    # 1. Zamieniamy krotki starych trójkątów na zbiory (robimy to raz przed pętlą dla szybkości)
                    s1, s2 = set(self.__triangles[t1].get_points()), set(self.__triangles[t2].get_points())

                    for new_tri, new_idx  in new_triangles:
                        new_set = set(new_tri.get_points())

                        if len(s1 & new_set) >= 2:
                            self.__triangles[t1].add_triangle_child(new_idx)

                        if len(s2 & new_set) >= 2:
                            self.__triangles[t2].add_triangle_child(new_idx)

                for t_id in new_triangles:
                    self.__triangulation.add(t_id)

                if self.__vis is not None:
                    for t_id in new_triangles:
                        vis_t = self.__vis.add_polygon(self.__points[list(self.__triangles[t_id].get_points())], color="green", fill=False)
                        self.__triangles[t_id].set_vis_polygon(vis_t)

                # Do tego miejsca zrefactorowane (bez DAG)

                for points in new_sections_points:
                    sec = find_sec_from_points(points)
                    legalize_edge(point, sec, self.__triangulation, build_graph, self.__vis)

            else: # punkt wewnątrz trójkąta
                p1,p2,p3 = curr_triangle.get_points()
                curr_triangle.destroy(self.__vis)
                Triangulation.remove(curr_triangle)

                for edge in curr_triangle.get_edges():
                    edge.remove_triangle(curr_triangle)


                new_triangles_points = [(p1, p2), (p2, p3), (p3, p1)]
                new_triangles = [Triangle(point, *points, build_graph) for points in new_triangles_points]

                for triangle in new_triangles:
                    Triangulation.add(triangle)

                if build_graph:
                    for triangle in new_triangles:
                        curr_triangle.children.add(triangle)

                if self.__vis is not None:
                    for t in new_triangles:
                        vis_t = self.__vis.add_polygon(self.__points[list(t.get_points())], color="green", fill=False)
                        t.set_vis_polygon(vis_t)

                edges: set['Section'] = set()
                for t in new_triangles:
                    edges |= t.get_edges()

                for edge in edges:
                    legalize_edge(point, edge, Triangulation, build_graph, self.__vis)

        def contain_initial_points(triangle: Triangle):
            nonlocal initial_triangle
            for p in triangle.get_points():
                if p in initial_triangle.get_points():
                    return True
            return False

        filtered_triangles = list(filter(contain_initial_points,Triangulation))
        if self.__vis is not None:
            for t in filtered_triangles:
                t.destroy(self.__vis)
            self.__vis.remove_figure(vis_initial_points)

    def get_triangulation(self):
        return self.__triangulation

    def get_initial_triangle(self, build_graph: bool) -> Triangle:
        """
        Dla danego zbioru punktów zwraca trójkąt, w którym zawarte są wszystkie punkty zbioru.
        """
        M = max(max(abs(self.__points[:, 0])), max(abs(self.__points[:, 1]))) + 1

        p1 = np.array([3.1 * M, 0])
        p2 = np.array([0, 3.1 * M])
        p3 = np.array([(-3.1) * M, (-3.1) * M])
        ind = len(self.__points)
        self.__points = np.vstack((self.__points, p1, p2, p3))

        INITIAL_ID = TriangleIndex(0)
        return Triangle((PointIndex(ind), PointIndex(ind+1), PointIndex(ind+2)), INITIAL_ID, build_graph)
