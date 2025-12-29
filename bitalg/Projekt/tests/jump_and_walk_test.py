import sys, os

from bitalg.Projekt.utils.Jump_And_Walk_Algorithm import jump_and_walk_next
from bitalg.Projekt.utils.Point import Point
from bitalg.Projekt.utils.Section import Section
from bitalg.Projekt.utils.Triangle import Triangle

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '../..')))
from bitalg.visualizer.main import Visualizer


def main():
    p1= Point(6, 0)
    p2= Point(3, 1)
    p3 = Point(8, 1)
    p4= Point(0, 4)
    p5= Point(2, 6)
    p6 = Point(1, 8)
    p7= Point(6, 10)
    p8= Point(8, 12)
    p9 = Point(7, 18)
    p10 = Point(4,4)
    px = Point(7,12)

    t1 = Triangle(p1,p2,p10)
    t2 = Triangle(p1,p3,p7)
    t3 = Triangle(p1,p10,p7)
    t4 = Triangle(p2,p10,p5)
    t5 = Triangle(p2,p4,p5)
    t6 = Triangle(p4,p5,p6)
    t7 = Triangle(p5,p6,p7)
    t8 = Triangle(p10,p5,p7)
    t9 = Triangle(p3,p7,p8)
    t10 = Triangle(p7,p8,p9)
    t11 = Triangle(p7,p9,p6)

    points: list['Point'] = [p1,p2,p3,p4,p5,p6,p7,p8,p9,p10]
    triangles: list['Triangle'] = [t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11]


    vis = Visualizer()
    for point in points:
        vis.add_point(point.get_cords(),color = "red")
    for triangle in triangles:
        vis.add_line_segment(triangle.get_list_edges(),color = "green")
    vis.add_point(px.get_cords(),color = "orange")
    vis.show()

    actual_triangle = triangles[4]
    while True:
        drawn_triangle = vis.add_polygon(actual_triangle.get_list_points(),color="blue",fill=True)
        next_triangle = jump_and_walk_next(px,actual_triangle)
        vis.remove_figure(drawn_triangle)
        if next_triangle == actual_triangle:
            break
        actual_triangle = next_triangle
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