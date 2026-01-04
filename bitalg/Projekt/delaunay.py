
from bitalg.Projekt.utils.classes.Point import Point
from bitalg.Projekt.utils.classes.Section import Section
from bitalg.Projekt.utils.classes.Triangle import Triangle
from bitalg.Projekt.utils.legality import legalize_edge, turned_points

from bitalg.Projekt.utils.orient import orient
from bitalg.Projekt.utils.find_sec_from_points import find_sec_from_points
from bitalg.Projekt.utils.search_triangulation import find_triangle_containing_point
from bitalg.visualizer.main import Visualizer

from typing import Union, Literal

def get_initial_triangle(points: list[Point], build_graph: bool) -> Triangle:
    """
    Dla danego zbioru punktów zwraca trójkąt, w którym zawarte są wszystkie punkty zbioru.
    """
    abs_cords = [cord for pt in points for cord in (abs(pt.get_x()), abs(pt.get_y()))]
    M = max(abs_cords)

    p1 = Point(3*M, 0) 
    p2 = Point(0, 3*M) 
    p3 = Point((-3)*M, (-3)*M)

    return Triangle(p1, p2, p3, build_graph)

def is_point_on_triangle_edge(p: Point, triangle: Triangle, eps = 1e-12) -> Union[bool, Section]:
    """
    Przyjmuje punkt oraz trójkąt. Jeżeli punkt leży na którejś z krawędzi trójkąta, zwraca tę krawędź,
    w przeciwnym razie zwraca False.
    """
    a, b, c = triangle.get_points()

    edges = [(a, b), (b, c), (c, a)]

    for edge in edges:
        det = orient(p, *edge)
        if abs(det) < eps: return find_sec_from_points(edge)
    return False

def triangulate(points: list[Point], variant: Literal["JaW", "Graph"]="JaW", vis: Visualizer = None) -> list[Triangle]:
    """
    Dla danego zbioru punktów zwraca triangulację Delaunaya tego zbioru
    Parametr variant odpowiada za wariant algorytmu wyszukiwania trójkąta który zawiera zadany punkt
    """

    build_graph = True if variant == "Graph" else False

    initial_triangle = get_initial_triangle(points, build_graph)
    Triangulation = [initial_triangle]

    if vis is not None:
        vis_initial_points = vis.add_point(initial_triangle.get_list_tuple_points(), color='orange')
        vis_initial_triangle = vis.add_polygon(initial_triangle.get_list_tuple_points(), color='green', fill=False)
        initial_triangle.set_vis_polygon(vis_initial_triangle)

    for point in points:
        if vis is not None:
            vis.add_point(point.get_cords(),color="red")

        curr_triangle = find_triangle_containing_point(point, Triangulation, variant, initial_triangle, vis)
        potential_edge = is_point_on_triangle_edge(point, curr_triangle)

        if potential_edge: # punkt na krawędzi trójkąta
            t1, t2 = tuple(potential_edge.get_triangles())
            i, j = potential_edge.get_ends()
            k, l = turned_points(potential_edge)
    
            t1.destroy(vis)
            t2.destroy(vis)
            Triangulation.remove(t1)
            Triangulation.remove(t2)

            new_sections_points = [(i, k), (i, l), (j, k), (j, l)]
            new_triangles = [Triangle(point, *points, build_graph) for points in new_sections_points]

            if build_graph:
                for triangle in new_triangles:
                    if triangle.get_edges().intersection(t1.get_edges()) != set():
                        t1.children.add(triangle)
                    if triangle.get_edges().intersection(t2.get_edges()) != set():
                        t2.children.add(triangle)

            for triangle in new_triangles:
                Triangulation.append(triangle)

            if vis is not None:
                for triangle in new_triangles:
                    vis_t = vis.add_polygon(triangle.get_list_tuple_points(), color="green", fill=False)
                    triangle.set_vis_polygon(vis_t)

            for points in new_sections_points:
                sec = find_sec_from_points(points)
                legalize_edge(point, sec, Triangulation, build_graph, vis)
   
        else: # punkt wewnątrz trójkąta
            p1,p2,p3 = curr_triangle.get_points()
            curr_triangle.destroy(vis)
            Triangulation.remove(curr_triangle)

            new_triangles_points = [(p1, p2), (p2, p3), (p3, p1)]
            new_triangles = [Triangle(point, *points, build_graph) for points in new_triangles_points]

            for triangle in new_triangles:
                Triangulation.append(triangle)

            if build_graph:
                for triangle in new_triangles:
                    curr_triangle.children.add(triangle)

            if vis is not None:
                for t in new_triangles:
                    vis_t = vis.add_polygon(t.get_list_tuple_points(), color="green", fill=False)
                    t.set_vis_polygon(vis_t)

            edges: set['Section'] = set()
            for t in new_triangles:
                edges |= t.get_edges()

            for edge in edges:
                legalize_edge(point, edge, Triangulation, build_graph, vis)

    def contain_initial_points(triangle: Triangle):
        nonlocal initial_triangle
        for p in triangle.get_points():
            if p in initial_triangle.get_points():
                return True
        return False

    filtered_triangles = list(filter(contain_initial_points,Triangulation))
    if vis is not None:
        for t in filtered_triangles:
            t.destroy(vis)
        vis.remove_figure(vis_initial_points)


    return list(set(Triangulation).difference(filtered_triangles))