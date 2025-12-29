from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from bitalg.Projekt.utils.Point import Point
    from bitalg.Projekt.utils.Section import Section


def orient(*args) -> float:
    # używamy własnej implementacji wyznacznika 2x2

    if len(args) ==3:
        p1,p2,p3 = args

    elif len(args) ==2:
        if isinstance(args[0],Section) and isinstance(args[1],Point):
            section = args[0]
            p3 = args[1]
        elif isinstance(args[0],Point) and isinstance(args[1],Section):
            section = args[1]
            p3 = args[0]
        else:
            raise ValueError("Provided {len(args)} arguments, expected Section and Point ")
        p1,p2 = section.get_tuple_ends()
    else:
        raise ValueError("Provided {len(args)} arguments, expected 2 or 3 arguments")

    ax, ay = p1.get_cords()
    bx, by = p2.get_cords()
    cx, cy = p3.get_cords()
    det = (ax - cx) * (by - cy) - (ay - cy) * (bx - cx)
    return det


