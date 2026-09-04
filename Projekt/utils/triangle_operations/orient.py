from Projekt.utils.custom_types import Point


def orient(points: tuple[Point,Point,Point]) -> float:
    # używamy własnej implementacji wyznacznika 2x2
    p1, p2, p3 = points
    ax, ay = p1
    bx, by = p2
    cx, cy = p3
    det = (ax - cx) * (by - cy) - (ay - cy) * (bx - cx)
    return det
