
from bitalg.Projekt.utils.classes.Point import Point
from bitalg.Projekt.utils.classes.Section import Section
from bitalg.Projekt.utils.classes.Triangle import Triangle
from bitalg.Projekt.utils.legality import legalize_edge

from bitalg.Projekt.utils.orient import orient
from bitalg.Projekt.utils.initial_triangle import get_initial_triangle
from bitalg.Projekt.utils.search_triangulation import find_triangle_containing_point

def is_point_on_triangle_edge(p: Point, triangle: Triangle, eps = 1e-12) -> bool:
    a, b, c = triangle.get_points()

    d1 = orient(p, a, b)
    d2 = orient(p, b, c)
    d3 = orient(p, c, a)

    return abs(d1) < eps or abs(d2) < eps or abs(d3) < eps




def triangulate(points: list[Point]) -> list[Triangle]:
    """
    Dla danego zbioru punktów zwraca triangulację Delaunaya tego zbioru
    """
    initial_triangle = get_initial_triangle(points)
    Triangles = [initial_triangle]

    n = len(points)

    for point in points:
        triangle = find_triangle_containing_point(point, Triangles, variant="JaW")
        
        if is_point_on_triangle_edge(point, triangle):
            pass
        else:
            triangle.destroy()
            p1,p2,p3 = triangle.get_points()
            Triangles.remove(triangle)
            t1 = Triangle(p1, p2, point)
            t2 = Triangle(p2, p3, point)
            t3 = Triangle(p3, p1, point)
            Triangles.append(t1)
            Triangles.append(t2)
            Triangles.append(t3)

            edges: set['Section'] = set()
            for t in (t1,t2,t3):
                edges |= t.get_edges()

            for edge in edges:
                legalize_edge(point,edge,Triangles)

    def not_contain_initial_points(triangle: Triangle):
        nonlocal initial_triangle
        for p in triangle.get_points():
            if p in initial_triangle.get_points():
                return False
        return True

    #
    # niedokończone
    #
    print("func")
    print("initial: ")
    print(initial_triangle)
    print("\n\n\nTriangles: ")
    print(Triangles)
    filtered_triangles = list(filter(not_contain_initial_points,Triangles))
    return filtered_triangles