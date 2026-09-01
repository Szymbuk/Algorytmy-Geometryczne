import numpy as np

def generate_circle_points(O, R, n = 100) -> np.ndarray:
    """
    Funkcja generuje jednostajnie n punktów na okręgu o środku O i promieniu R
    :param O: tablica współrzędnych x, y określająca środek okręgu
    :param R: promień okręgu
    :param n: ilość generowanych punktów
    :return: tablica punktów w postaci dwuelementowych tablic współrzędnych
    """
    theta_s = np.random.uniform(0.0,2*np.pi,n)
    x_s = O[0] + R * np.cos(theta_s)
    y_s = O[1] + R*np.sin(theta_s)
    res = np.column_stack((x_s,y_s))

    return res

