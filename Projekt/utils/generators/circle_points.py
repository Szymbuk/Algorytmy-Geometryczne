import random
import math
def generate_circle_points(O, R, n = 100) -> list[tuple[float,float]]:
    """
    Funkcja generuje jednostajnie n punktów na okręgu o środku O i promieniu R
    :param O: krotka współrzędnych x, y określająca środek okręgu
    :param R: promień okręgu
    :param n: ilość generowanych punktów
    :return: tablica punktów w postaci krotek współrzędnych
    """
    tab = []
    for i in range(n):
        theta = random.uniform(0,2*math.pi)
        x = O[0] + R*math.cos(theta)
        y = O[1] + R*math.sin(theta)
        tab.append((x,y))
    return tab
