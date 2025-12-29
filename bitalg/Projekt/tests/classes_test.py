import sys, os

from bitalg.Projekt.utils.Point import Point
from bitalg.Projekt.utils.Section import Section
from bitalg.Projekt.utils.Triangle import Triangle

sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '../..')))
from bitalg.visualizer.main import Visualizer


def main():
    p1= Point(5, 4, 1)
    p2= Point(3, 0, 2)
    p3 = Point(1, 7, 3)
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


if __name__ == "__main__":
    main()