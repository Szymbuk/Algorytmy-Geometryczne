from bitalg.Projekt.utils.classes.Point import Point
from bitalg.Projekt.utils.classes.Section import Section
from bitalg.Projekt.utils.classes.Triangle import Triangle

from typing import Literal
from bitalg.Projekt.utils.jump_and_walk import jump_and_walk_triangle_search
from bitalg.Projekt.utils.directed_graph_dfs import dfs_trianglation
from bitalg.visualizer.main import Visualizer


def find_triangle_containing_point(point: Point, T: list[Triangle], variant: Literal["JaW", "Graph"], initial_triangle: Triangle, vis: Visualizer = None) -> Triangle:
    """
    Zwraca trójkąt triangulacji który zawiera dany punkt, możliwe są dwa warianty 
    czyli dwa różne algorytmy znajdowania tego trójkąta:
    "JaW" - Jump and Walk
    "Graph" - Wyszukiwanie w strukturze acyklicznego skierowanego grafu trójkątów
    """
    if variant == "JaW":
        return jump_and_walk_triangle_search(point, T, vis)
    elif variant == "Graph":
        return dfs_trianglation(point, initial_triangle, vis)
    else:
        raise ValueError(f'Wariant "{variant}" algorytmu wyszukiwania nie istnieje.')


