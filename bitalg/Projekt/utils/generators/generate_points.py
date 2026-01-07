import random
from bitalg.Projekt.utils.classes.Point import Point

def generate_uniform_points(left=-100, right=100, n=100) -> list[Point]:
    result = []
    for _ in range(n):
        x = random.uniform(left,right)
        y = random.uniform(left,right)
        result.append(Point(x,y))

    return result