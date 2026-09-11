import numpy as np
from Projekt.utils.custom_types import PointIndex, TriangleIndex, EPSILON
from Projekt.utils.triangle_operations.orient import orient
    
    
def test_orient_clockwise():
    p1 = np.array([0.0, 0.0])
    p2 = np.array([1.0, 0.0])
    p3 = np.array([0.5, -1.0])

    assert orient((p1, p2, p3)) < -EPSILON
    
    
def test_orient_counterClockwise():
    p1 = np.array([0.0, 0.0])
    p2 = np.array([1.0, 0.0])
    p3 = np.array([-0.5, 1.0])

    assert orient((p1, p2, p3)) > EPSILON
    
def test_orient_collinear():
    p1 = np.array([0.0, 0.0])
    p2 = np.array([1.0, 0.0])
    p3 = np.array([2.0, 0.0])
    p4 = np.array([3.0, 1e-14])
    p5 = np.array([3.0, 1e-12])   

    assert abs(orient((p1, p2, p3))) < EPSILON
    assert abs(orient((p1, p2, p4))) < EPSILON
    assert abs(orient((p1, p3, p5))) > EPSILON # false for 1e-13 and smaller