from typing import Literal,List

from bitalg.visualizer.main import Visualizer

from Projekt.utils.custom_types import EdgeAdjacencyMap, TriangleIndex, PointIndex, PointsArray, variants,Triangle
from Projekt.utils.triangle_search.jump_and_walk import jump_and_walk_triangle_search
from Projekt.utils.triangle_search.directed_graph_dfs import dfs_trianglation


def find_triangle_containing_point(point: PointIndex, variant: variants,points_array: PointsArray,adjacency_graph: EdgeAdjacencyMap, triangles: List[Triangle], children_graph: list[set[TriangleIndex]], vis: Visualizer| None = None) -> TriangleIndex:
    """
    Zwraca trójkąt triangulacji który zawiera dany punkt, możliwe są dwa warianty 
    czyli dwa różne algorytmy znajdowania tego trójkąta:
    "JaW" - Jump and Walk
    "Graph" - Wyszukiwanie w strukturze acyklicznego skierowanego grafu trójkątów
    """
    
    # Initial triangle is the first triangle in the list of triangles, which is the supertriangle that contains all points.
    if variant == "JaW":
        return jump_and_walk_triangle_search(point,points_array,adjacency_graph,triangles,  vis)
    elif variant == "Graph":
        return dfs_trianglation(point, TriangleIndex(0), triangles, children_graph, points_array, vis)
    else:
        raise ValueError(f'Wariant "{variant}" algorytmu wyszukiwania nie istnieje.')


