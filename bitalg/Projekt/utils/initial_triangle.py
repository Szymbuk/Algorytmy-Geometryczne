from bitalg.Projekt.utils.classes.Point import Point
from bitalg.Projekt.utils.classes.Triangle import Triangle

def get_initial_triangle(points: list[Point]) -> Triangle:
    """
    Dla danej chmury punktów zwraca trójkąt, w którym zawarte są wszystkie punkty chmury.
    """
    abs_cords = [cord for pt in points for cord in (abs(pt.get_x()), abs(pt.get_y()))]
    M = max(abs_cords)

    p1 = Point(3*M, 0) 
    p2 = Point(0, 3*M) 
    p3 = Point((-3)*M, (-3)*M)

    return Triangle(p1, p2, p3)
    

