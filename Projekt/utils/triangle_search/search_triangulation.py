

from Projekt.utils.Triangle import Triangle

from typing import Literal,List

from Projekt.utils.custom_types import EdgeAdjacencyMap, TriangleIndex
from Projekt.utils.triangle_search.jump_and_walk import jump_and_walk_triangle_search
from Projekt.utils.triangle_search.directed_graph_dfs import dfs_trianglation
from bitalg.visualizer.main import Visualizer
from Projekt.utils.custom_types import PointIndex, PointsArray


def find_triangle_containing_point(point: PointIndex, variant: Literal["JaW", "Graph"], initial_triangle: Triangle,points_array: PointsArray,adjacency_graph: EdgeAdjacencyMap, triangles: List[Triangle], vis: Visualizer = None) -> TriangleIndex:
    """
    Zwraca trójkąt triangulacji który zawiera dany punkt, możliwe są dwa warianty 
    czyli dwa różne algorytmy znajdowania tego trójkąta:
    "JaW" - Jump and Walk
    "Graph" - Wyszukiwanie w strukturze acyklicznego skierowanego grafu trójkątów
    """
    if variant == "JaW":
        return jump_and_walk_triangle_search(point,points_array,adjacency_graph,triangles,  vis)
    elif variant == "Graph":
        return dfs_trianglation(point, initial_triangle, vis)
    else:
        raise ValueError(f'Wariant "{variant}" algorytmu wyszukiwania nie istnieje.')


