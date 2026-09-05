import sys, os
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '../..')))

from Projekt.utils.triangle_search.jump_and_walk import jump_and_walk_next
from Projekt.utils.custom_types import PointsArray
from Projekt.utils.Triangle import Triangle
import numpy as np


from bitalg.visualizer.main import Visualizer


def main():
    p1 = np.array([6, 0])
    p2 = np.array([3, 1])
    p3 = np.array([8, 1])
    p4 = np.array([0, 4])
    p5 = np.array([2, 6])
    p6 = np.array([1, 8])
    p7 = np.array([6, 10])
    p8 = np.array([8, 12])
    p9 = np.array([7, 18])
    p10= np.array([4, 4])
    px = np.array([7, 12])

    points: PointsArray = np.array([p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, px])

    t1 = Triangle((0, 9, 1))
    t2 = Triangle((0, 2, 6))
    t3 = Triangle((0, 6, 9))
    t4 = Triangle((1, 9, 4))
    t5 = Triangle((1, 4, 3))
    t6 = Triangle((3, 4, 5))
    t7 = Triangle((4, 6, 5))
    t8 = Triangle((9, 6, 4))
    t9 = Triangle((2, 7, 6))
    t10= Triangle((6, 7, 8))
    t11= Triangle((6, 8, 5))


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
        next_triangle = jump_and_walk_next(10,actual_triangle,points,adjacency_graph)

        vis.remove_figure(drawn_triangle)
        if next_triangle == actual_triangle:
            break
        actual_triangle = next_triangle
    vis.axis_equal()
    vis.show_gif(400)
    vis.save_gif("gifs/animacja1",interval=400)


if __name__ == "__main__":
    main()