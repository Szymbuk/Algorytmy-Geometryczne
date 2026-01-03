from bitalg.Projekt.delaunay import triangulate
from bitalg.Projekt.utils.classes.Point import Point
from bitalg.Projekt.utils.generate_points import generate_uniform_points
from bitalg.Projekt.utils.initial_triangle import get_initial_triangle
from bitalg.visualizer.main import Visualizer


def test():
    vis = Visualizer()

    points = [Point(2,0),Point(1,2),Point(0,0),Point(1,1)]
    #points = generate_uniform_points(-1000,1000,10)
    initial_triangle = get_initial_triangle(points)
    print(points)
    triangles =triangulate(points,vis)
    print(triangles)



    vis.show()
    vis.save_gif("simple_test",interval=500)


if __name__ == "__main__":
    test()