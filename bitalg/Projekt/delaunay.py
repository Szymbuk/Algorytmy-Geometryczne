
from bitalg.Projekt.utils.classes.Point import Point
from bitalg.Projekt.utils.classes.Section import Section
from bitalg.Projekt.utils.classes.Triangle import Triangle
from bitalg.Projekt.utils.legality import legalize_edge, turned_points

from bitalg.Projekt.utils.orient import orient
from bitalg.Projekt.utils.search_triangulation import find_triangle_containing_point, find_sec_in_T
from bitalg.visualizer.main import Visualizer

from typing import Union

def get_initial_triangle(points: list[Point]) -> Triangle:
    """
    Dla danego zbioru punktów zwraca trójkąt, w którym zawarte są wszystkie punkty zbioru.
    """
    abs_cords = [cord for pt in points for cord in (abs(pt.get_x()), abs(pt.get_y()))]
    M = max(abs_cords)

    p1 = Point(3*M, 0) 
    p2 = Point(0, 3*M) 
    p3 = Point((-3)*M, (-3)*M)

    return Triangle(p1, p2, p3)

def is_point_on_triangle_edge(p: Point, triangle: Triangle, eps = 1e-12) -> Union[bool, Section]:
    """
    Przyjmuje punkt oraz trójkąt. Jeżeli punkt leży na którejś z krawędzi trójkąta, zwraca tę krawędź,
    w przeciwnym razie zwraca False.
    """
    a, b, c = triangle.get_points()

    edges = [(a, b), (b, c), (c, a)]

    for edge in edges:
        det = orient(p, *edge)
        if abs(det) < eps: return find_sec_in_T(edge)
    return False

def triangulate(points: list[Point], vis: Visualizer = None) -> list[Triangle]:
    """
    Dla danego zbioru punktów zwraca triangulację Delaunaya tego zbioru
    """
    initial_triangle = get_initial_triangle(points)
    Triangles = [initial_triangle]

    if vis is not None:
        vis_initial_points = vis.add_point(initial_triangle.get_list_tuple_points(), color='orange')
        vis_initial_triangle = vis.add_polygon(initial_triangle.get_list_tuple_points(), color='green', fill=False)
        initial_triangle.set_vis_polygon(vis_initial_triangle)

    for point in points:
        if vis is not None:
            vis.add_point(point.get_cords(),color="red")

        triangle = find_triangle_containing_point(point, Triangles, variant="JaW")
        potential_edge = is_point_on_triangle_edge(point, triangle)

        if potential_edge: # punkt na krawędzi trójkąta
            t1, t2 = tuple(potential_edge.get_triangles())
            i, j = potential_edge.get_ends()
            k, l = turned_points(potential_edge)
    
            t1.destroy(vis)
            t2.destroy(vis)
            Triangles.remove(t1)
            Triangles.remove(t2)

            new_sections_points = [(i, k), (i, l), (j, k), (j, l)]
            new_triangles = [Triangle(point, *points) for points in new_sections_points]
            if vis is not None:
                for triangle in new_triangles:
                    vis_t = vis.add_polygon(triangle.get_list_tuple_points(),color="green",fill=False)
                    triangle.set_vis_polygon(vis_t)

            
            for triangle in new_triangles:
                Triangles.append(triangle)

            for points in new_sections_points:
                sec = find_sec_in_T(points)
                legalize_edge(point, sec, vis)
   
        else: # punkt wewnątrz trójkąta
            p1,p2,p3 = triangle.get_points()
            triangle.destroy(vis)
            Triangles.remove(triangle)

            new_triangles_points = [(p1, p2), (p2, p3), (p3, p1)]
            new_triangles = [Triangle(point, *points) for points in new_triangles_points]

            for triangle in new_triangles:
                Triangles.append(triangle)

            if vis is not None:
                for t in new_triangles:
                    vis_t = vis.add_polygon(t.get_list_tuple_points(), color="green", fill=False)
                    t.set_vis_polygon(vis_t)

            edges: set['Section'] = set()
            for t in new_triangles:
                edges |= t.get_edges()

            for edge in edges:
                legalize_edge(point, edge, vis)

    def contain_initial_points(triangle: Triangle):
        nonlocal initial_triangle
        for p in triangle.get_points():
            if p in initial_triangle.get_points():
                return True
        return False


    # print("func")
    # print("initial: ")
    # print(initial_triangle)
    # print("\n\n\nTriangles: ")
    # print(Triangles)
    filtered_triangles = list(filter(contain_initial_points,Triangles))
    if vis is not None:
        for t in filtered_triangles:
            t.destroy(vis)
        vis.remove_figure(vis_initial_points)

    return list(set(Triangles).difference(filtered_triangles))