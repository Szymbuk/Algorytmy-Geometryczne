import numpy as np
from numpy import dtype
import pandas as pd
import matplotlib.pyplot as plt
import random
import sys, os
import time
sys.path.append(os.path.abspath(os.path.join(os.getcwd(), '../..')))
from bitalg.tests.test1 import Test
from bitalg.visualizer.main import Visualizer
import math
import sys, os
import time


def draw_example():
    vis = Visualizer()
    vis.add_line(((0, 2), (10, 7)))
    vis.add_point((4, 4), s=30, color='purple')
    vis.add_point((6, 6), s=30, color='green')
    vis.add_point((7, 4), s=30, color='orange')
    vis.show()
