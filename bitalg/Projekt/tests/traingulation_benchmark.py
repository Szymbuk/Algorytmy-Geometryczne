from bitalg.Projekt.utils.classes.Point import Point, EPSILON
from bitalg.Projekt.utils.classes.Section import Section
from bitalg.Projekt.utils.classes.Triangle import Triangle
from bitalg.Projekt.utils.legality import legalize_edge, turned_points

from bitalg.Projekt.utils.orient import orient
from bitalg.Projekt.utils.find_sec_from_points import find_sec_from_points
from bitalg.Projekt.utils.search_triangulation import find_triangle_containing_point
from bitalg.visualizer.main import Visualizer

from typing import Union, Literal
import time
import matplotlib.pyplot as plt
from bitalg.Projekt.utils.generate_points import generate_uniform_points


def get_initial_triangle(points: list[Point], build_graph: bool) -> Triangle:
    """
    Dla danego zbioru punktów zwraca trójkąt, w którym zawarte są wszystkie punkty zbioru.
    """
    abs_cords = [cord for pt in points for cord in (abs(pt.get_x()), abs(pt.get_y()))]
    M = max(abs_cords)

    p1 = Point(3 * M, 0)
    p2 = Point(0, 3 * M)
    p3 = Point((-3) * M, (-3) * M)

    return Triangle(p1, p2, p3, build_graph)


def is_point_on_triangle_edge(p: Point, triangle: Triangle) -> Union[bool, Section]:
    """
    Przyjmuje punkt oraz trójkąt. Jeżeli punkt leży na którejś z krawędzi trójkąta, zwraca tę krawędź,
    w przeciwnym razie zwraca False.
    """
    a, b, c = triangle.get_points()

    edges = [(a, b), (b, c), (c, a)]

    for edge in edges:
        det = orient(p, *edge)
        if abs(det) < EPSILON: return find_sec_from_points(edge)
    return False


def triangulate_benchmark(points: list[Point], variant: Literal["JaW", "Graph"] = "JaW"):
    """
    Dla danego zbioru punktów zwraca triangulację Delaunaya tego zbioru
    Parametr variant odpowiada za wariant algorytmu wyszukiwania trójkąta, który zawiera zadany punkt
    """

    stats = {
        "search_time": 0.0,
        "update_time": 0.0,
        "total_time": 0.0
    }

    start_algorithm = time.time()

    build_graph = True if variant == "Graph" else False

    initial_triangle = get_initial_triangle(points, build_graph)
    Triangulation = [initial_triangle]



    for point in points:

        t0 = time.time()
        curr_triangle = find_triangle_containing_point(point, Triangulation, variant, initial_triangle, None)
        t1 = time.time()
        stats["search_time"] += (t1 - t0)

        t2 = time.time()
        potential_edge = is_point_on_triangle_edge(point, curr_triangle)

        if potential_edge:  # punkt na krawędzi trójkąta
            t1, t2 = tuple(potential_edge.get_triangles())
            i, j = potential_edge.get_ends()
            k, l = turned_points(potential_edge)

            t1.destroy(None)
            t2.destroy(None)
            Triangulation.remove(t1)
            Triangulation.remove(t2)

            new_sections_points = [(i, k), (i, l), (j, k), (j, l)]
            new_triangles = [Triangle(point, *points, build_graph) for points in new_sections_points]

            if build_graph:
                for triangle in new_triangles:
                    if triangle.get_edges().intersection(t1.get_edges()) != set():
                        t1.children.add(triangle)
                    if triangle.get_edges().intersection(t2.get_edges()) != set():
                        t2.children.add(triangle)

            for triangle in new_triangles:
                Triangulation.append(triangle)



            for points in new_sections_points:
                sec = find_sec_from_points(points)
                legalize_edge(point, sec, Triangulation, build_graph, None)

        else:  # punkt wewnątrz trójkąta
            p1, p2, p3 = curr_triangle.get_points()
            curr_triangle.destroy(None)
            Triangulation.remove(curr_triangle)

            new_triangles_points = [(p1, p2), (p2, p3), (p3, p1)]
            new_triangles = [Triangle(point, *points, build_graph) for points in new_triangles_points]

            for triangle in new_triangles:
                Triangulation.append(triangle)

            if build_graph:
                for triangle in new_triangles:
                    curr_triangle.children.add(triangle)

            edges: set['Section'] = set()
            for t in new_triangles:
                edges |= t.get_edges()

            for edge in edges:
                legalize_edge(point, edge, Triangulation, build_graph, None)

        t3 = time.time()
        stats["update_time"] += (t3 - t2)

    end_algorithm = time.time()
    stats["total_time"] = end_algorithm - start_algorithm

    def contain_initial_points(triangle: Triangle):
        nonlocal initial_triangle
        for p in triangle.get_points():
            if p in initial_triangle.get_points():
                return True
        return False

    filtered_triangles = list(filter(contain_initial_points, Triangulation))
    return list(set(Triangulation).difference(filtered_triangles)),stats






def run_performance_analysis():
    # 1. Konfiguracja eksperymentu
    # Dla Pythona "duże zbiory" to np. do 10k-20k punktów (powyżej może trwać minuty)
    sizes = [100, 500, 1000, 2000, 5000, 10000,50000,100000]

    results = [{
        "n": [],
        "search": [],
        "update": [],
        "total": []
    },{
        "n": [],
        "search": [],
        "update": [],
        "total": []
    }
    ]
    variants = ["JaW","Graph"]

    print(f"{'N':<10} | {'Search [s]':<12} | {'Update [s]':<12} | {'Total [s]':<12}")
    print("-" * 55)
    for i in range(len(variants)):
        print(variants[i])
        for n in sizes:
            # Generowanie danych
            points = generate_uniform_points(-1000, 1000, n)

            # Uruchomienie algorytmu (bez wizualizacji!)
            # stats = triangulate_with_stats(points, variant="JaW")


            import random
            stats = triangulate_benchmark(points,variants[i])[1]


            results[i]["n"].append(n)
            results[i]["search"].append(stats["search_time"])
            results[i]["update"].append(stats["update_time"])
            results[i]["total"].append(stats["total_time"])

            print(f"{n:<10} | {stats['search_time']:<12.4f} | {stats['update_time']:<12.4f} | {stats['total_time']:<12.4f}")

    return results


def plot_results(results):
    n = results["n"]
    search = results["search"]
    update = results["update"]

    # Wykres 1: Liniowy porównawczy
    plt.figure(figsize=(10, 6))
    plt.plot(n, search, label='Lokalizacja punktu (Search)', marker='o')
    plt.plot(n, update, label='Aktualizacja struktury (Flip)', marker='s')
    plt.xlabel('Liczba punktów')
    plt.ylabel('Czas [s]')
    plt.title('Porównanie czasu etapów algorytmu Delaunaya')
    plt.legend()
    plt.grid(True)
    plt.savefig("efficiency_line_chart.png")
    plt.show()

    # Wykres 2: Skumulowany (Stacked Area/Bar) - pokazuje udział procentowy
    plt.figure(figsize=(10, 6))
    plt.stackplot(n, search, update, labels=['Search', 'Update'], alpha=0.7)
    plt.xlabel('Liczba punktów')
    plt.ylabel('Czas [s]')
    plt.title('Skumulowany czas wykonania')
    plt.legend(loc='upper left')
    plt.grid(True, linestyle='--')
    plt.savefig("efficiency_stacked_chart.png")
    plt.show()


if __name__ == "__main__":
    data = run_performance_analysis()
    plot_results(data[0])
    plot_results(data[1])