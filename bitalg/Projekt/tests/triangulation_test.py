from bitalg.Projekt.delaunay import triangulate
from bitalg.Projekt.utils.classes.Point import Point
from bitalg.Projekt.utils.generate_points import generate_uniform_points
from bitalg.visualizer.main import Visualizer


def test():
    vis = Visualizer()

    #points = [Point(0,0),Point(2,0),Point(1,2),Point(1,1)]
    """points = [Point(-561.9652499078964, -882.1804597099914), Point(-574.7043288894524, 543.6102623684917),
     Point(-192.6445520872337, 436.2953913056633), Point(-392.43052187171475, 714.8911722194955),
     Point(982.4793494799846, 301.28839450867645), Point(142.31806631726863, 991.4265854655255),
     Point(772.5480889358421, 1.1270877495277318), Point(531.14473138741, -939.9785373783234),
     Point(228.8220999435382, -755.0493446072966), Point(536.0253450471314, 428.73024476700857)]
     """
    points = generate_uniform_points(-1000,1000,10)
    print(points)
    triangles =triangulate(points,vis)
    print(triangles)
    #vis.add_polygon(list(map(lambda x: x.get_list_tuple_points(),triangles)),fill=False,color="green")


    vis.axis_equal()
    vis.show()
    vis.save_gif("simple_test",interval=500)


if __name__ == "__main__":
    test()