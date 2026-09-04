import sys, os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '../..')))

from Projekt.utils.triangle_search.jump_and_walk import jump_and_walk_next
from Projekt.utils.custom_types import Point,PointsArray
from Projekt.utils.classes.Triangle import Triangle
import numpy as np


from bitalg.visualizer.main import Visualizer


def main():
    p0 = np.array([0, 0])
    p1 = np.array([6, 0])
    p2 = np.array([3, 1])
    p3 = np.array([8, 1])
    p4 = np.array([0, 4])
    p5 = np.array([2, 6])
    p6 = np.array([1, 8])
    p7 = np.array([6, 10])
    p8 = np.array([8, 12])
    p9 = np.array([7, 18])
    p10 = np.array([4, 4])
    px = np.array([7, 12])

    points: PointsArray = np.array([p0, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, px])

    t1 = Triangle((1, 10, 2))
    t2 = Triangle((1, 3, 7))
    t3 = Triangle((1, 7, 10))
    t4 = Triangle((2, 10, 5))
    t5 = Triangle((2, 5, 4))
    t6 = Triangle((4, 5, 6))
    t7 = Triangle((5, 7, 6))
    t8 = Triangle((10, 7, 5))
    t9 = Triangle((3, 8, 7))
    t10 = Triangle((7, 8, 9))
    t11 = Triangle((7, 9, 6))


    triangles: list['Triangle'] = [t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11]

    adjacency_graph = {}
    for triangle in triangles:
        p1, p2, p3 = triangle.get_points()
        edges = [(p1, p2), (p2, p3), (p3, p1)]
        edges = list(map(lambda edge: tuple(sorted(edge)), edges))
        for edge in edges:
            if edge not in adjacency_graph:
                adjacency_graph[edge] = []
            adjacency_graph[edge].append(triangle)


    vis = Visualizer()
    for point in points:
        vis.add_point(point,color = "red")
    for triangle in triangles:
        p1, p2, p3 = points[list(triangle.get_points())]
        edges = [(p1, p2), (p2, p3), (p3, p1)]
        vis.add_line_segment(edges,color = "green")
    vis.add_point(px,color = "orange")
    vis.show()

    actual_triangle = triangles[4]
    while True:
        drawn_triangle = vis.add_polygon(points[list(actual_triangle.get_points())], color="blue", fill=True)
        vis.show()
        next_triangle = jump_and_walk_next(11,actual_triangle,points,adjacency_graph)

        vis.remove_figure(drawn_triangle)
        if next_triangle == actual_triangle:
            break
        actual_triangle = next_triangle
    vis.axis_equal()
    vis.show_gif(400)
    vis.save_gif("animacja1",interval=400)





    """
    print(p1)
    sec1= Section(p1, p2, 1)
    sec2 = Section(p2, p3, 2)
    sec3= Section(p1, p3, 3)
    print(sec1)
    t1 = Triangle(p1, p2, p3)
    print(t1)

    vis = Visualizer()

    T1 = Triangle(p1, p2, p3)
    print()

    q, r = T1.define_circle()
    print("Circle parameters: ", q, r)
    vis.add_circle([q.get_cords()[0], q.get_cords()[1], r], fill=False, color="green")
    vis.add_point(q.get_cords(), color="orange")
    vis.add_point([p1.get_cords(), p2.get_cords(), p3.get_cords()], color="orange")
    vis.add_line_segment(T1.get_list_edges(), color="red")
    vis.show()
    vis.show_gif()
    """


if __name__ == "__main__":
    main()