from bitalg.Projekt.delaunay import triangulate
from bitalg.Projekt.utils.classes.Point import Point
from bitalg.Projekt.utils.generators.generate_points import generate_uniform_points
from bitalg.visualizer.main import Visualizer

def test():
    vis = Visualizer()
    vis.set_limits(xlim=(-10, 10), ylim=(-10, 10))
    #points = [Point(0,0),Point(2,0),Point(1,2),Point(1,1)]
    """points = [Point(-561.9652499078964, -882.1804597099914), Point(-574.7043288894524, 543.6102623684917),
     Point(-192.6445520872337, 436.2953913056633), Point(-392.43052187171475, 714.8911722194955),
     Point(982.4793494799846, 301.28839450867645), Point(142.31806631726863, 991.4265854655255),
     Point(772.5480889358421, 1.1270877495277318), Point(531.14473138741, -939.9785373783234),
     Point(228.8220999435382, -755.0493446072966), Point(536.0253450471314, 428.73024476700857)]"""
    """points = [
    Point(2, 3),  # p1 (Lewy dolny bazy)
    Point(6, 3),  # p2 (Prawy dolny bazy)
    Point(4, 6),  # p3 (Szczyt - tworzy z p1,p2 trójkąt niemal równoboczny)
    Point(4, 2),  # p4 (Wpada w okrąg p1-p2-p3, wymusza FLIP krawędzi p1-p2)
    Point(7, 5),  # p5 (Dodatkowy punkt z boku, żeby nie było zbyt symetrycznie)
    Point(1, 5)   # p6 (Dodatkowy punkt z drugiej strony)
]"""
    #points = generate_uniform_points(-10,10,5000)
    points = [Point(0,0),Point(2,0),Point(0,2),Point(2,2),Point(-2,0),Point(0,-2),Point(-2,-2),Point(-2,2),Point(2,-2)]
    print(points)
    triangles =triangulate(points,"JaW",vis)


    print(triangles)
    #vis.add_polygon(list(map(lambda x: x.get_list_tuple_points(),triangles)),fill=False,color="green")


    vis.axis_equal()
    vis.show()
    #vis.save_gif("random",interval=500)


if __name__ == "__main__":
    test()