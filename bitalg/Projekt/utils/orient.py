
def orient(*args) -> float:
    # używamy własnej implementacji wyznacznika 2x2

    if len(args) != 3:
        raise ValueError("Oczekiwano 3 punktów")

    p1, p2, p3 = args

    try:
        ax, ay = p1.get_cords()
        bx, by = p2.get_cords()
        cx, cy = p3.get_cords()
    except:
        raise AttributeError("Dostarczone obiekty nie są punktami")
    
    det = (ax - cx) * (by - cy) - (ay - cy) * (bx - cx)
    return det
