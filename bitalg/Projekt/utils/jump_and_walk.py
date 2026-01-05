from bitalg.Projekt.utils.classes.Point import Point, EPSILON
from bitalg.Projekt.utils.classes.Triangle import Triangle
from bitalg.Projekt.utils.orient import orient
from bitalg.visualizer.main import Visualizer
import random


def jump_and_walk_triangle_search(point: Point, triangles: set[Triangle], vis: Visualizer = None) -> Triangle:
    if not hasattr(jump_and_walk_triangle_search, "last_triangle"):
        jump_and_walk_triangle_search.last_triangle = None

        # Próbujemy użyć ostatniego trójkąta jako startowego
    actual_triangle = jump_and_walk_triangle_search.last_triangle

    # Walidacja: Musimy sprawdzić, czy ten trójkąt nadal istnieje!
    # (Mógł zostać usunięty w procesie flipowania w poprzednim kroku).
    # Sprawdzenie 'in set' jest w Pythonie bardzo szybkie O(1).
    if actual_triangle is None or actual_triangle not in triangles:
        # Fallback: Jeśli cache jest pusty lub nieaktualny, bierzemy dowolny ze zbioru
        for t in triangles:
            actual_triangle = t
            break

    # Zabezpieczenie przed pętlą nieskończoną
    steps = 0
    max_steps = len(triangles)   + 1# Pesymistycznie nie powinniśmy odwiedzić więcej niż N trójkątów

    while steps <= max_steps:
        next_triangle = jump_and_walk_next(point, actual_triangle)
        if next_triangle == actual_triangle:
            jump_and_walk_triangle_search.last_triangle = actual_triangle
            return actual_triangle
        actual_triangle = next_triangle
        steps+=1

    print("Warning: Jump-and-Walk failed, switching to brute-force.")
    jump_and_walk_triangle_search.last_triangle = None
    for t in triangles:

        p1, p2, p3 = t.get_points()
        if (orient(p1, p2, point) >= -EPSILON and
                orient(p2, p3, point) >= -EPSILON and
                orient(p3, p1, point) >= -EPSILON):
            return t
    raise ValueError("Punkt poza granicami triangulacji")

def jump_and_walk_next(point: Point, triangle:Triangle) -> Triangle:
    p1, p2, p3 = triangle.get_points()
    pairs = [(p1, p2), (p2, p3), (p3, p1)]

    edge = None
    for a, b in pairs:
        det = orient(a, b, point)
        if det < -EPSILON:
            edges = a.get_edges()
            for sample_edge in edges:
                if b in sample_edge.get_ends():
                    edge = sample_edge
                    break
            break 
    else:
        return triangle 

    try:
        t1, t2 = list(edge.get_triangles())
        return t1 if triangle == t2 else t2
    except ValueError: # w wypadku gdy jest tylko jeden sąsiadujący trójkąt
        return triangle
