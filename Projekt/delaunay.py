import numpy as np
from typing import Union, Literal

from bitalg.visualizer.main import Visualizer

from Projekt.utils.custom_types import Point, PointIndex, PointsArray, TriangleIndex, EdgeAdjacencyMap, variants, EPSILON
from Projekt.utils.custom_types import Triangle
from Projekt.utils.triangle_operations.legality import legalize_edge, turned_points
from Projekt.utils.triangle_operations.orient import orient
from Projekt.utils.triangle_search.search_triangulation import find_triangle_containing_point
from Projekt.utils.triangle_search.directed_graph_dfs import dfs_trianglation_point
from Projekt.utils.triangle_search.jump_and_walk import jump_and_walk_point_search
from Projekt.utils.triangle_operations.create_triangle import make_ccw_triangle


class Triangulation:
    def __init__(self, points: PointsArray, variant: variants= "JaW", vis: Visualizer | None = None):
        self.__points = points
        self.__variant: variants = variant
        self.__triangulation: set[TriangleIndex] = set({}) # set of triangle t_id's
        self.__adjacency_graph: EdgeAdjacencyMap = {}
        self.__vis = vis
        self.__triangles: list[Triangle] = [] # A list of all triangles created during the triangulation process, indexed by their t_id's.
        self.__children_graph: list[set[TriangleIndex]] = [] # A list of sets, where each set contains the t_id's of the children triangles of the triangle at that index.
        self.__vis_triangle_objects = [] # A list of visualizer polygon objects corresponding to the triangles in self.__triangles. If a triangle has no visualizer object.
        


    def is_point_on_triangle_edge(self,px: Point, triangle_id: TriangleIndex) -> Union[None, tuple[PointIndex, PointIndex]]:
        """
        Przyjmuje punkt oraz trójkąt. Jeżeli punkt leży na którejś z krawędzi trójkąta, zwraca tę krawędź,
        w przeciwnym razie zwraca False.
        """
        a, b, c = self.__triangles[triangle_id]

        edges = [tuple(sorted((a, b))), tuple(sorted((b, c))), tuple(sorted((c, a)))]

        for edge in edges:
            p1,p2 = self.__points[list(edge)]
            det = orient((p1,p2,px))
            if abs(det) < EPSILON:
                if edge[0] < edge[1]:
                    return edge[0],edge[1]
                else:
                    return edge[1],edge[0]
        return None

    def triangulate(self) -> None:
        """
        Dla danego zbioru punktów zwraca triangulację Delaunay tego zbioru.
        Parametr variant odpowiada za wariant algorytmu wyszukiwania trójkąta, który zawiera zadany punkt
        """

        build_graph = True if self.__variant == "Graph" else False

        initial_triangle: Triangle = self.get_initial_triangle(build_graph)
        self.__triangles.append(initial_triangle)

        init_id = TriangleIndex(0)
        self.__triangulation.add(init_id)
        self.__children_graph.append(set())
        
        p1,p2,p3 = self.__triangles[init_id]
        for p_0,p_1 in [(p1,p2),(p2,p3),(p3,p1)]:
            if p_0 > p_1:
                p_0, p_1 = p_1, p_0
            self.__adjacency_graph[(p_0,p_1)] = [init_id]

        vis_initial_points = None
        vis_initial_triangle = None
        if self.__vis is not None:
            vis_initial_points = self.__vis.add_point(self.__points[[p1,p2,p3]], color='orange')
            vis_initial_triangle = self.__vis.add_polygon(self.__points[[p1,p2,p3]], color='green', fill=False)
            self.__vis_triangle_objects.append(vis_initial_triangle)

        for point_ind, point in enumerate(self.__points[:-3]): # Exclude the last three points which are the vertices of the initial triangle
            point: Point
            point_ind =  PointIndex(point_ind)
            print(f"Dodawanie punktu {point_ind}: {point}")
            if self.__vis is not None:
                self.__vis.add_point(point, color="red")

            curr_triangle_id = find_triangle_containing_point(point_ind,self.__variant,self.__points, self.__adjacency_graph,self.__triangles,self.__children_graph,  self.__vis)
            potential_edge = self.is_point_on_triangle_edge(point, curr_triangle_id)

            if potential_edge: # punkt na krawędzi trójkąta

                # removing from the adjacency graph.
                i, j = potential_edge
                k, l = turned_points(i, j, self.__adjacency_graph, self.__triangles)
                t1, t2 = self.__adjacency_graph.pop(potential_edge)

                for triangle_id in (t1, t2):
                    triangle = self.__triangles[triangle_id]
                    for p_0, p_1 in ((triangle[0], triangle[1]),
                                     (triangle[1], triangle[2]),
                                     (triangle[2], triangle[0])):
                        
                        if p_0 > p_1:
                            p_0, p_1 = p_1, p_0
                        edge = (p_0, p_1)
                        triangle_ids = self.__adjacency_graph.get(edge)
                        if triangle_ids is None:
                            continue
                        triangle_ids.remove(triangle_id)
                        if not triangle_ids:
                            del self.__adjacency_graph[edge]

                # removing a vis object of triangle.
                self.__triangles[t1]
                if self.__vis is not None:
                    if self.__vis_triangle_objects[t1] is not  None and self.__vis_triangle_objects[t2] is not None:  
                        self.__vis.remove_figure(self.__vis_triangle_objects[t1])
                        self.__vis.remove_figure(self.__vis_triangle_objects[t2])
                        self.__vis_triangle_objects[t1] = None
                        self.__vis_triangle_objects[t2] = None
                    else:
                        raise ValueError("Próba usunięcia ze sceny obiektu, który nie posiada referencji do obiektu sceny")

                self.__triangulation.remove(t1)
                self.__triangulation.remove(t2)

                new_triangles: list[TriangleIndex] = []
                new_sections_points = [(i, k), (i, l), (j, k), (j, l)]
                for p1,p2 in new_sections_points:
                    self.create_triangle(p1, p2, point_ind, new_triangles)

                if build_graph:
                    # 1. Zamieniamy krotki starych trójkątów na zbiory (robimy to raz przed pętlą dla szybkości)
                    s1, s2 = set(self.__triangles[t1]), set(self.__triangles[t2])

                    for new_idx  in new_triangles:
                        new_set = set(self.__triangles[new_idx])

                        if len(s1 & new_set) >= 2:
                            self.__children_graph[t1].add(new_idx)

                        if len(s2 & new_set) >= 2:
                            self.__children_graph[t2].add(new_idx)

                for new_id in new_triangles:
                    self.__triangulation.add(new_id)

                if self.__vis is not None:
                    for new_id in new_triangles:
                        vis_t = self.__vis.add_polygon(self.__points[list(self.__triangles[new_id])], color="green", fill=False)
                        self.__vis_triangle_objects.append(vis_t)

                # Do tego miejsca odświeżono
                for section in new_sections_points:
                    legalize_edge(point_ind, section, self.__triangulation, self.__adjacency_graph, self.__triangles, self.__points,build_graph, self.__children_graph, self.__vis, self.__vis_triangle_objects)

            else: # punkt wewnątrz trójkąta
                p1,p2,p3 = self.__triangles[curr_triangle_id]
                if self.__vis is not None:
                    if self.__vis_triangle_objects[curr_triangle_id] is not None:
                        self.__vis.remove_figure(self.__vis_triangle_objects[curr_triangle_id])
                    else:
                        raise ValueError("Próba usunięcia ze sceny obiektu, który nie posiada referencji do obiektu sceny")
                self.__triangulation.remove(curr_triangle_id)
                if self.__vis is not None:
                    self.__vis_triangle_objects[curr_triangle_id] = None


                new_triangles_points = [(p1, p2), (p2, p3), (p3, p1)]
                new_triangles = []
                for px,py in new_triangles_points:
                    if px>py:
                        px,py = py,px
                    
                    self.__adjacency_graph[(px,py)].remove(curr_triangle_id)
                    self.create_triangle(px, py, point_ind, new_triangles)
                    


                if build_graph:
                    for triangle_ind in new_triangles:
                        self.__children_graph[curr_triangle_id].add(triangle_ind)

                if self.__vis is not None:
                    for t_ind in new_triangles:
                        vis_t = self.__vis.add_polygon(self.__points[list(self.__triangles[t_ind])], color="green", fill=False)
                        self.__vis_triangle_objects.append(vis_t)


                for edge in new_triangles_points:
                    legalize_edge(point_ind, edge, self.__triangulation, self.__adjacency_graph, self.__triangles, self.__points, build_graph, self.__children_graph, self.__vis, self.__vis_triangle_objects)

        triangles_to_remove = []
        p1, p2, p3 = self.__triangles[TriangleIndex(0)]
        for t_id in self.__triangulation:
            triangle = self.__triangles[t_id]
            if p1 in triangle or p2 in triangle or p3 in triangle:
                triangles_to_remove.append(t_id)
        for t_id in triangles_to_remove:
            self.__triangulation.remove(t_id)
            if self.__vis is not None:
                if self.__vis_triangle_objects[t_id] is not None:
                    self.__vis.remove_figure(self.__vis_triangle_objects[t_id])
                    self.__vis_triangle_objects[t_id] = None
                    
        for edge, triangle_ids in list(self.__adjacency_graph.items()):
            triangle_ids[:] = [
                t_id
                for t_id in triangle_ids
                if t_id not in triangles_to_remove
            ]

            if not triangle_ids:
                del self.__adjacency_graph[edge]

        if self.__vis is not None:
            if vis_initial_triangle is not None:
                self.__vis.remove_figure(vis_initial_triangle)
            if vis_initial_points is not None:
                self.__vis.remove_figure(vis_initial_points)

    def get_triangulation(self):
        return [self.__triangles[triangle_id] for triangle_id in sorted(self.__triangulation)]

    def find_triangle(self, point: Point, variant: variants  = "JaW", trace: bool = False):
        """Zwraca aktywny trójkąt zawierający punkt, używając wybranego algorytmu."""
        # query = np.asarray(point)
        if point.shape != (2,):
            raise ValueError("Punkt musi mieć dokładnie dwie współrzędne.")

        selected_variant = variant or self.__variant
        if selected_variant not in ("JaW", "Graph"):
            raise ValueError(f'Wariant "{selected_variant}" algorytmu wyszukiwania nie istnieje.')

        if selected_variant == "Graph" and not self.__children_graph[0]:
            raise ValueError("Wariant Graph wymaga triangulacji zbudowanej z grafem dzieci.")

        try:
            if selected_variant == "JaW":
                triangle_id, visited = jump_and_walk_point_search(point, self.__points, self.__adjacency_graph, self.__triangles)
            else:
                triangle_id, visited = dfs_trianglation_point(point, TriangleIndex(0), self.__triangles, self.__children_graph, self.__points)
        except RuntimeError as error:
            raise ValueError(f"Punkt {point} nie należy do triangulacji.") from error

        if triangle_id not in self.__triangulation:
            raise ValueError(f"Punkt {point} nie należy do triangulacji.")

        result = (triangle_id, self.__triangles[triangle_id])
        return (*result, visited) if trace else result

    def get_triangles(self):
        return self.get_triangulation()

    def get_triangle_ids(self):
        return self.__triangulation.copy()

    def get_initial_triangle(self, build_graph: bool) -> Triangle:
        """
        Dla danego zbioru punktów zwraca trójkąt, w którym zawarte są wszystkie punkty zbioru.
        """
        M = max(max(abs(self.__points[:, 0])), max(abs(self.__points[:, 1]))) + 1

        p1 = np.array([3.1 * M, 0])
        p2 = np.array([0, 3.1 * M])
        p3 = np.array([(-3.1) * M, (-3.1) * M])
        ind = PointIndex(len(self.__points))
        self.__points = np.vstack((self.__points, p1, p2, p3))
        t = make_ccw_triangle(ind, PointIndex(ind + 1), PointIndex(ind + 2), self.__points)
        return t
    
    def create_triangle(self, p1: PointIndex, p2: PointIndex, point_ind: PointIndex, new_triangles: list[TriangleIndex]) -> None:
        t = make_ccw_triangle(p1, p2, point_ind,self.__points)
        new_id = TriangleIndex(len(self.__triangles))


        new_triangles.append(new_id)
        self.__triangles.append(t)
        self.__triangulation.add(new_id)
        self.__children_graph.append(set())
        
        if len(self.__triangles) != len(self.__children_graph):
            raise RuntimeError("Niepoprawna długość listy trójkątów i listy grafu dzieci.")
        

        for px,py in [(p1,p2),(p2,point_ind),(p1,point_ind)]:
            if px > py:
                px,py = py,px
            if (px,py) not in self.__adjacency_graph:
                self.__adjacency_graph[px,py] = [new_id]
            else:
                self.__adjacency_graph[px,py].append(new_id)
                if len(self.__adjacency_graph[px,py]) > 2:
                    raise RuntimeError(f"Niepoprawna liczba trójkątów w grafie sąsiedztwa dla krawędzi: {(px,py)}")
