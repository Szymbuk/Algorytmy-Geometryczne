from typing import List

import numpy as np
import math
from Projekt.utils.custom_types import PointIndex, TriangleIndex, Triangle, PointsArray, EdgeAdjacencyMap, Point
from Projekt.utils.triangle_operations.create_triangle import make_ccw_triangle
from bitalg.visualizer.main import Visualizer

def turned_points(p1: PointIndex,p2: PointIndex,adjacency_graph: EdgeAdjacencyMap,triangles: List[Triangle]) -> tuple[PointIndex,PointIndex]:
    """
    Zwraca punkty, które byłyby końcami odcinka po jego przekręceniu
    """
    if p1>p2:
        p1,p2 = p2,p1
    t1, t2 = adjacency_graph[(p1,p2)]
    points: set[PointIndex] = set()
    points.update(triangles[t1])
    points.update(triangles[t2])

    points.remove(p1)
    points.remove(p2)
    px,py = tuple(points)
    
    return px,py

def turn(sec: tuple[PointIndex, PointIndex], build_graph: bool, triangulation: set[TriangleIndex],adjacency_graph: EdgeAdjacencyMap, triangles: List[Triangle],children_graph: list[set[TriangleIndex]], points: PointsArray, vis: Visualizer | None, vis_polygons: list) -> None:
    """
    Dokonuje "przekręcenia" krawędzi w triangulacji
    """
    p1, p2 = sec
    p3, p4 = turned_points(p1, p2, adjacency_graph, triangles)
    
    if p1>p2:
        p1,p2 = p2,p1
    t1, t2 = adjacency_graph[(p1,p2)]


    triangulation.remove(t1)
    px,py,pz = triangles[t1]
    for p_0,p_1 in [(px,py),(py,pz),(pz,px)]:
        if p_0>p_1:
            p_0,p_1 = p_1,p_0
        adjacency_graph[(p_0,p_1)].remove(t1)
    
    triangulation.remove(t2)
    px,py,pz = triangles[t2]
    for p_0,p_1 in [(px,py),(py,pz),(pz,px)]:
        if p_0>p_1:
            p_0,p_1 = p_1,p_0
        adjacency_graph[(p_0,p_1)].remove(t2)
    
    if vis is not None:
        vis.remove_figure(vis_polygons[t1])
        vis.remove_figure(vis_polygons[t2])
        vis_polygons[t1] = None
        vis_polygons[t2] = None


    l = len(triangles)
    new_t1_id = TriangleIndex(l)
    new_t2_id = TriangleIndex(l+1)
    
    for p_0,p_1 in [(p1,p3),(p3,p4),(p4,p1)]:
        if p_0>p_1:
            p_0,p_1 = p_1,p_0
        adjacency_graph.setdefault((p_0,p_1), []).append(new_t1_id)
    for p_0,p_1 in [(p2,p3),(p3,p4),(p4,p2)]:
        if p_0>p_1:
            p_0,p_1 = p_1,p_0
        adjacency_graph.setdefault((p_0,p_1), []).append(new_t2_id)
        
        
    new_t1 = make_ccw_triangle(p1, p3, p4, points)
    new_t2 = make_ccw_triangle(p2, p3, p4, points)
    triangles.append(new_t1)
    triangles.append(new_t2)
    children_graph.extend((set(), set()))
    
    triangulation |= set([new_t1_id, new_t2_id])
    

    if build_graph:
        children_graph[t1] |= set([new_t1_id, new_t2_id])
        children_graph[t2] |= set([new_t1_id, new_t2_id])

    if vis is not None:
        p1_ind , p2_ind, p3_ind = triangles[new_t1_id]
        p1, p2, p3 = points[p1_ind], points[p2_ind], points[p3_ind]
        vis_t1 = vis.add_polygon([p1, p2, p3], fill=False, color="green")
        
        
        p1_ind , p2_ind, p3_ind = triangles[new_t2_id]
        p1, p2, p3 = points[p1_ind], points[p2_ind], points[p3_ind]
        vis_t2 = vis.add_polygon([p1, p2, p3], fill=False, color="green")
        
        vis_polygons.append(vis_t1)
        vis_polygons.append(vis_t2)


    return

def is_legal(point: PointIndex, sec: tuple[PointIndex, PointIndex], adjacency_graph: EdgeAdjacencyMap, triangles: List[Triangle], points: PointsArray) -> bool:
    """
    Zwraca czy krawędź jest legalna, to znaczy czy mogłaby być częścią triangulacji delaunaya
    """
    i,j = sec
    if i>j:
        i,j = j,i
    t1, t2 = tuple(adjacency_graph[(i,j)])

    if point in triangles[t1]:
        containing_triangle_id, other_triangle_id = t1, t2
    elif point in triangles[t2]:
        containing_triangle_id, other_triangle_id = t2, t1
    else:
        raise ValueError(f"Punkt {point} nie należy do żadnego trójkąta przy krawędzi {(i, j)}")

    triangle_points = points[list(triangles[containing_triangle_id])]
    center, radius = define_circle(*triangle_points)
    opposite_point = next(vertex for vertex in triangles[other_triangle_id] if vertex not in (i, j))

    distance = np.linalg.norm(points[opposite_point] - center)
    return distance> radius


def define_circle(p1: Point,p2: Point,p3: Point) -> tuple[np.ndarray, float]:
    # korzystając z równania okręgu x^2 + y^2 + Dx + Ey + F = 0

    A = np.array([[p1[0],p1[1],1],
                    [p2[0], p2[1], 1],
                    [p3[0], p3[1], 1]
                    ])
    b = np.array([-(p1[0]**2 + p1[1]**2),
                    -(p2[0] ** 2 + p2[1] ** 2),
                    -(p3[0] ** 2 + p3[1] ** 2),
                    ])
    try:
        x = np.linalg.solve(A,b)
    except np.linalg.LinAlgError:
        # Punkty współliniowe - okrąg ma nieskończony promień.
        # Zwracamy "bezpieczną" wartość, punkt bardzo daleko
        return np.array([1e6, 1e6]), float('inf')


    D,E,F = x

    x0 = -D/2
    y0 = -E/2

    r = math.sqrt(x0**2 + y0**2 - F)

    return np.array([x0,y0]),r

def legalize_edge(point: PointIndex, sec: tuple[PointIndex, PointIndex], triangulation: set[TriangleIndex],adjacency_graph: EdgeAdjacencyMap,triangles: List[Triangle],points: PointsArray, build_graph: bool,children_graph: list[set[TriangleIndex]], vis: Visualizer | None, vis_polygons: list) -> None:
    i, j = sec
    if i>j:
        i,j = j,i
        
    if len(adjacency_graph[(i,j)]) < 2: # nie chcemy obracać odcinków będących na zewnątrz (należących do otoczki)
        return



    p1, p2 = turned_points(i,j,adjacency_graph,triangles)

    k = p2 if p1 == point else p1

    # dodane w celu braku błedu, gdyby vis się zmieniło.
    vis_segment = None
    vis_circle = None
    
    if vis is not None:
        circle_triangle = None
        for triangle_ind in adjacency_graph[(i,j)]:
            if point in triangles[triangle_ind]:
                circle_triangle = triangles[triangle_ind]
        if circle_triangle is None:
            raise ValueError("Nie ma takiego trójkąta")
    
        px_ind, py_ind, pz_ind = circle_triangle
        px,py,pz = points[px_ind], points[py_ind], points[pz_ind]
        circle_center, radius = define_circle(px, py, pz)
        vis_circle = vis.add_circle([circle_center[0],circle_center[1],radius],fill=False,color="purple")
        vis_segment =vis.add_line_segment([points[sec[0]],points[sec[1]]],color="red")

    if not is_legal(point, sec, adjacency_graph, triangles, points):
        
        vis_new_segment = None
        if vis is not None:
            vis.remove_figure(vis_segment)
            vis_new_segment = vis.add_line_segment([points[p1],points[p2]],color='red')
            vis.remove_figure(vis_circle)





        turn(sec, build_graph,triangulation,adjacency_graph,triangles,children_graph,points, vis,vis_polygons)

        if i>k:
            i,k = k,i
        if j>k:
            j,k = k,j
            
        sec1 = (i, k)
        sec2 = (j, k)


        if vis is not None:
            if p1>p2:
                p1,p2 = p2,p1
            new_sec = (p1, p2)

            if new_sec not in adjacency_graph:
                raise ValueError(f"Nie ma krawędzi {new_sec}")
            new_circle_triangle2 = None
            new_circle_triangle = None



            if new_sec[0]>new_sec[1]:
                new_sec = (new_sec[1],new_sec[0])

            new_circle_triangle,new_circle_triangle2 = adjacency_graph[new_sec]
            if new_circle_triangle is None:
                raise ValueError("Nie ma takiego trójkąta")

            p1_ind,p2_ind,p3_ind = triangles[new_circle_triangle]
            p1,p2,p3 = points[p1_ind], points[p2_ind], points[p3_ind]
            circle_center, radius = define_circle(p1, p2, p3)
            if new_circle_triangle2 is not None:
                p1_ind,p2_ind,p3_ind = triangles[new_circle_triangle2]
                p1,p2,p3 = points[p1_ind], points[p2_ind], points[p3_ind]
                circle_center2, radius2 = define_circle(p1, p2, p3)
                
                new_vis_circle2 = vis.add_circle([circle_center2[0], circle_center2[1], radius2], fill=False, color="purple")
                #vis.show()
                vis.remove_figure(new_vis_circle2)

            new_vis_circle = vis.add_circle([circle_center[0], circle_center[1], radius], fill=False, color="purple")

            #vis.show()
            vis.remove_figure(new_vis_circle)
            vis.remove_figure(vis_new_segment)





        legalize_edge(point, sec1, triangulation, adjacency_graph,triangles,points, build_graph, children_graph, vis, vis_polygons)
        legalize_edge(point, sec2, triangulation, adjacency_graph,triangles,points, build_graph, children_graph, vis, vis_polygons)

    elif vis is not None:
        vis.remove_figure(vis_circle)
        vis.remove_figure(vis_segment)


