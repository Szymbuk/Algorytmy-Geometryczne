from bitalg.Projekt.utils.Point import Point
from bitalg.Projekt.utils.Triangle import Triangle
from bitalg.Projekt.utils.orient import orient


def jump_and_walk_triangle_search(point: Point,triangles: list[Triangle]) -> Triangle:
    actual_triangle = triangles[0]
    """

    while True:
        p1,p2,p3 = actual_triangle.get_points()
        end = False

        # sprawdzamy brzegi trójkąta
        for edge in p1.get_edges():
            if point.on_section(edge):
                end = True
        for edge in p2.get_edges():
            if point.on_section(edge):
                end = True

        # sprawdzamy wnętrze trójkąta
        orient1 = orient(p1,p2,point)
        orient2 = orient(p2,p3,point)
        orient3 = orient(p3,p1,point)
        if orient1> 0 and orient2>0 and orient3>0:
            end = True

        if end:
            break


        if orient1<0:
            edge1,edge2 = list(p1.get_edges())
            if p2 in edge1.get_ends():
                edge = edge1
            else:
                edge = edge2

        elif orient2<0:
            edge1,edge2 = list(p2.get_edges())
            if p3 in edge1.get_ends():
                edge = edge1
            else:
                edge = edge2

        else:
            edge1,edge2 = list(p3.get_edges())
            if p1 in edge1.get_ends():
                edge = edge1
            else:
                edge = edge2


        t1,t2 = list(edge.get_triangle())

        if actual_triangle ==t1:
            actual_triangle = t2
        else:
            actual_triangle = t1
    """

    while True:
        next_triangle = jump_and_walk_next(point,actual_triangle)
        if next_triangle == actual_triangle:
            return actual_triangle
        actual_triangle = next_triangle





def jump_and_walk_next(point: Point,triangle :Triangle) -> Triangle:
    p1, p2, p3 = triangle.get_points()
    end = False
    orient1 = orient(p1, p2, point)
    orient2 = orient(p2, p3, point)
    orient3 = orient(p3, p1, point)


    if orient1 < 0:
        edges = list(p1.get_edges())
        for sample_edge in edges:
            if p2 in sample_edge.get_ends():
                edge = sample_edge


    elif orient2 < 0:
        edges = list(p2.get_edges())
        for sample_edge in edges:
            if p3 in sample_edge.get_ends():
                edge = sample_edge

    elif orient3<0:
        edges = list(p3.get_edges())
        for sample_edge in edges:
            if p1 in sample_edge.get_ends():
                edge = sample_edge
    else:
        return triangle


    t1, t2 = list(edge.get_triangle())
    if triangle == t1:
        triangle = t2
    else:
        triangle = t1
    return triangle
