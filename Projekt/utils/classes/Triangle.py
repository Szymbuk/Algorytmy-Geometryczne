# from Projekt.utils.triangle_operations.find_sec_from_points import find_sec_from_points
# from Projekt.utils.triangle_operations.orient import orient
from bitalg.visualizer.main import Visualizer
from Projekt.utils.custom_types import PointIndex
import math

EPSILON = 1e-12
class Triangle:

    def __init__(self, points: tuple[PointIndex,PointIndex,PointIndex], build_graph: bool=False, vis_polygon = None):
        self.__points = points
        self.__vis_polygon = vis_polygon

        if build_graph:
            self.children: set[PointIndex] = set()

        if len(points) != 3:
            raise TypeError("Należy podać krotkę 3 punktów.\n Podano {}".format(type(points)))

    def set_points(self, points: tuple[PointIndex,PointIndex,PointIndex]) -> None:
        """
        Przypisuje nowe punkty oraz krawędzie danemu trójkątowi
        """
        self.__points = points

    def get_points(self) -> tuple[PointIndex,PointIndex,PointIndex]:
        return self.__points

    # def define_circle(self) -> tuple[np.ndarray, float]:
    #     # korzystając z równania okręgu x^2 + y^2 + Dx + Ey + F = 0
    #
    #     p1,p2,p3 = self.__points
    #     A = np.array([[p1.get_x(),p1.get_y(),1],
    #                  [p2.get_x(), p2.get_y(), 1],
    #                  [p3.get_x(), p3.get_y(), 1]
    #                   ])
    #     b = np.array([-(p1.get_x()**2 + p1.get_y()**2),
    #                  -(p2.get_x() ** 2 + p2.get_y() ** 2),
    #                  -(p3.get_x() ** 2 + p3.get_y() ** 2),
    #                  ])
    #     try:
    #         x = np.linalg.solve(A,b)
    #     except np.linalg.LinAlgError:
    #         # Punkty współliniowe - okrąg ma nieskończony promień.
    #         # Zwracamy "bezpieczną" wartość, punkt bardzo daleko
    #         return np.array([1e6, 1e6]), float('inf')
    #
    #
    #     D,E,F = x
    #
    #     x0 = -D/2
    #     y0 = -E/2
    #
    #     r = math.sqrt(x0**2 + y0**2 - F)
    #
    #     return np.array([x0,y0]),r

    def destroy(self, vis: Visualizer = None):
        """
        Usuwa referencje z powiązanych krawędzi do danego trójkąta,
        jeżeli podano obiekt sceny, obiekt jest z niej usuwany
        """
        if vis is not None:
            if self.__vis_polygon is None:
                raise ValueError("Próba usunięcia ze sceny obiektu, który nie posiada referencji do obiektu sceny")
            vis.remove_figure(self.__vis_polygon)
        # for edge in self.__edges:
        #     edge.remove_triangle(self)

    def set_vis_polygon(self, vis_polygon):
        """
        Przypisuje referencję do obiektu sceny
        """
        self.__vis_polygon = vis_polygon

    def  __repr__(self) -> str:
        return f"Triangle: {self.__points} \n"

    def __eq__(self, other):
        if not isinstance(other, Triangle):
            return False
        return set(self.__points) == set(other.get_points())






