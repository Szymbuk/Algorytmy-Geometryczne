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

def func():
    points = [(3,4),(2,1),(3,8)]
    vis = Visualizer()
    vis.add_point(points)
    vis.show()

if __name__ == "main":
    func()
