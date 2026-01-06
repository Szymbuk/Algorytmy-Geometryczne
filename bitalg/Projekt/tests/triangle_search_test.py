from bitalg.Projekt.delaunay import triangulate
from bitalg.Projekt.utils.generate_points import generate_uniform_points
import time

def test():

    numbers = [100,1e3,1e4,1e5,1e6,5*1e6]

    for i in range(len(numbers)):

        n = int(numbers[i])
        print("Number of points: ",n)
        points = generate_uniform_points(-1000000, 1000000, n)
        start = time.time()
        triangulate(points,"Graph")
        stop = time.time()
        print("JaW: ",stop-start)
        start = time.time()
        triangulate(points,"JaW")
        stop = time.time()
        print("Graph: ",stop-start)
        print("\n")

if __name__ == '__main__':
    test()