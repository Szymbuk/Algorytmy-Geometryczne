from bitalg.Projekt.utils.classes.Point import Point
from bitalg.Projekt.utils.classes.Section import Section
from bitalg.Projekt.utils.classes.Triangle import Triangle
from bitalg.Projekt.utils.legality import is_legal, turn, legalize_edge
from bitalg.visualizer.main import Visualizer


def test1():
    p1,p2,p3,p4 = Point(1,2),Point(2,4),Point(6,2),Point(7,7)
    s1,s2,s3,s4,s5 = Section(p1,p2),Section(p2,p4),Section(p3,p4),Section(p3,p1),Section(p1,p4)
    triangles = [Triangle(p1,p2,p4),Triangle(p4,p3,p1)]
    vis = Visualizer()
    vis.add_point([p1.get_cords(),p2.get_cords(),p3.get_cords(),p4.get_cords()],color="red")

    polygs = vis.add_polygon([t.get_list_tuple_points() for t in triangles], color="green", fill=False)
    vis.show()
    print(triangles)
    print(is_legal(s5))
    if not is_legal(s5):
        turn(s5,False,triangles,None)
    print(triangles)
    vis.remove_figure(polygs)
    vis.add_polygon([t.get_list_tuple_points() for t in triangles], color="green", fill=False)
    vis.axis_equal()
    vis.show()


def test2():
    p1,p2,p3,p4 = Point(1,2),Point(2,4),Point(6,2),Point(7,7)
    s1,s2,s3,s4,s5 = Section(p1,p2),Section(p2,p4),Section(p3,p4),Section(p3,p1),Section(p1,p4)
    triangles = [Triangle(p1,p2,p4),Triangle(p4,p3,p1)]
    vis = Visualizer()
    vis.add_point([p1.get_cords(),p2.get_cords(),p3.get_cords(),p4.get_cords()],color="red")

    polygs = vis.add_polygon([t.get_list_tuple_points() for t in triangles], color="green", fill=False)
    vis.show()
    #print(triangles)
    #print(is_legal(s5))
    legalize_edge(p1,s5,triangles,None,None)
    #print(triangles)
    vis.remove_figure(polygs)
    vis.add_polygon([t.get_list_tuple_points() for t in triangles], color="green", fill=False)
    vis.axis_equal()
    vis.show()




if __name__ == "__main__":
    test1()
    #test2()