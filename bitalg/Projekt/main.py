import random
import math
import matplotlib.pyplot as plt
from sortedcontainers import SortedList


from bitalg.tests.test4 import Test
from bitalg.visualizer.main import Visualizer

if __name__ == "__main__":
    points = [(3,4),(2,1),(3,8)]
    vis = Visualizer();
    vis.add_point(points)
    vis.show()
