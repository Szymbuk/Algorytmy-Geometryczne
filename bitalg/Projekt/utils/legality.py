from bitalg.Projekt.utils.classes.Point import Point
from bitalg.Projekt.utils.classes.Section import Section
from bitalg.Projekt.utils.classes.Triangle import Triangle

from bitalg.Projekt.utils.find_sec_from_points import find_sec_from_points
from bitalg.visualizer.main import Visualizer

def turned_points(sec: Section) -> set[Point]:
    """
    Zwraca punkty, które byłyby końcami odcinka po jego przekręceniu
    """
    t1, t2 = tuple(sec.get_triangles())
    edges = t1.get_edges() | t2.get_edges()
    points = set()
    for edge in edges:
        points |= edge.get_ends()

    new_sec_pts = points.difference(sec.get_ends())
    
    return new_sec_pts

def turn(sec: Section, build_graph: bool, T: set[Triangle], vis: Visualizer) -> tuple[Point, Point]:
    """
    Dokonuje "przekręcenia" krawędzi w triangulacji
    """
    t1, t2 = tuple(sec.get_triangles())
    sec_pts = sec.get_ends()
    new_sec_pts = turned_points(sec)

    p1, p2 = tuple(sec_pts)
    p3, p4 = tuple(new_sec_pts)

    p1.remove_edge(sec)
    p2.remove_edge(sec)

    t1.destroy(vis)
    t2.destroy(vis)

    new_triangles = (
        Triangle(p1, p3, p4, build_graph),
        Triangle(p2, p3, p4, build_graph)
    )
    T |= set(new_triangles)

    T.remove(t1)
    T.remove(t2)

    if build_graph:
        t1.children |= set(new_triangles)
        t2.children |= set(new_triangles)

    if vis is not None:
        new_t1, new_t2 = new_triangles
        vis_t1 = vis.add_polygon(new_t1.get_list_tuple_points(),fill=False,color="green")
        vis_t2 = vis.add_polygon(new_t2.get_list_tuple_points(),fill=False,color="green")
        new_t1.set_vis_polygon(vis_t1)
        new_t2.set_vis_polygon(vis_t2)


    return p3, p4

def is_legal(sec: Section) -> bool:
    """
    Zwraca czy krawędź jest legalna, to znaczy czy mogłaby być częścią triangulacji delaunaya
    """
    t1, t2 = tuple(sec.get_triangles())
    
    new_sec_pts = turned_points(sec)
    p1, p2 = tuple(new_sec_pts)

    center, radius = t1.define_circle()
    point = p2 if p1 in t1.get_points() else p1
    
    return not point.in_circle(center, radius)

def legalize_edge(point: Point, sec: Section, T: set[Triangle], build_graph: bool, vis: Visualizer) -> None:
    if len(sec.get_triangles())<2: # nie chcemy obracać odcinków będących na zewnątrz (należących do otoczki)
        return

    sec_pts = sec.get_ends()
    new_sec_pts = turned_points(sec)

    i, j = tuple(sec_pts) 
    p1, p2 = tuple(new_sec_pts)

    k = p2 if p1 == point else p1

    if vis is not None:
        circle_triangle = None
        for triangle in sec.get_triangles():
            if point in triangle.get_points():
                circle_triangle = triangle
        if circle_triangle is None:
            raise ValueError("Nie ma takiego trójkąta")

        circle_center, radius = circle_triangle.define_circle()
        vis_circle = vis.add_circle([circle_center.get_x(),circle_center.get_y(),radius],fill=False,color="purple")
        vis_segment =vis.add_line_segment(sec.get_tuple_ends(),color="red")

    if not is_legal(sec):
        if vis is not None:
            vis.show()
            vis.remove_figure(vis_segment)
            vis_new_segment = vis.add_line_segment((p1.get_cords(),p2.get_cords()),color='red')
            vis.remove_figure(vis_circle)

        turn(sec, build_graph, T, vis)

        sec1 = find_sec_from_points((i, k))
        sec2 = find_sec_from_points((j, k))

        if vis is not None:

            new_sec = None
            for edge in p1.get_edges():
                if p2 in edge.get_ends():
                    new_sec = edge
            if new_sec is None:
                raise ValueError("Nie ma takiego odcinka")
            new_circle_triangle2 = None
            new_circle_triangle = None
            """

            for triangle in new_sec.get_triangles():
                if point in triangle.get_points():
                    new_circle_triangle = triangle
                else:
                    new_circle_triangle2 = triangle
            """
            new_circle_triangle,new_circle_triangle2 = new_sec.get_triangles()
            if new_circle_triangle is None:
                raise ValueError("Nie ma takiego trójkąta")

            circle_center, radius = new_circle_triangle.define_circle()
            if new_circle_triangle2 is not None:
                circle_center2, radius2 = new_circle_triangle2.define_circle()

            new_vis_circle = vis.add_circle([circle_center.get_x(), circle_center.get_y(), radius], fill=False, color="purple")

            vis.show()
            vis.remove_figure(new_vis_circle)
            if new_circle_triangle2 is not None:
                new_vis_circle2 = vis.add_circle([circle_center2.get_x(), circle_center2.get_y(), radius2], fill=False, color="purple")
                vis.show()
                vis.remove_figure(new_vis_circle2)

            vis.remove_figure(vis_new_segment)


        legalize_edge(point, sec1, T, build_graph, vis)
        legalize_edge(point, sec2, T, build_graph, vis)

    elif vis is not None:
        vis.remove_figure(vis_circle)
        vis.remove_figure(vis_segment)


