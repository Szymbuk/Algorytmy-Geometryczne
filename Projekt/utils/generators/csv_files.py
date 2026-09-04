import csv
# from Projekt.utils.classes.Point import Point
from Projekt.utils.classes.Triangle import Triangle
import numpy as np
from Projekt.utils.custom_types import Point,PointsArray


# --- OBSŁUGA PUNKTÓW ---

def save_points_to_csv(points: PointsArray, filename: str):
    """
    Zapisuje listę obiektów Point do pliku CSV.
    Format: id,x,y
    """
    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['id', 'x', 'y'])  # Nagłówek

            for i,p in enumerate(points):
                writer.writerow([i, p[0], p[1]])
        print(f"Pomyślnie zapisano {len(points)} punktów do {filename}")
    except IOError as e:
        print(f"Błąd zapisu punktów: {e}")


def load_points_from_csv(filename: str) -> PointsArray:
    """
    Wczytuje punkty z pliku CSV i zwraca listę obiektów Point.
    """
    points = []
    try:
        with open(filename, mode='r', newline='', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            next(reader, None)  # Pomijamy nagłówek

            for row in reader:
                if row:
                    x = np.float64(row[1])
                    y = np.float64(row[2])
                    points.append(np.array([x, y]))
        print(f"Pomyślnie wczytano {len(points)} punktów z {filename}")
        return np.array(points)
    except FileNotFoundError:
        print(f"Plik {filename} nie istnieje.")
        return np.array([])
    except ValueError as e:
        print(f"Błąd formatu danych w pliku CSV: {e}")
        return np.array([])


def save_triangulation_to_csv(triangles: list[Triangle], filename: str):
    """
    Zapisuje triangulację (listę trójkątów) do CSV.
    Zapisuje ID punktów składowych: p1_id, p2_id, p3_id
    """
    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['p1_id', 'p2_id', 'p3_id'])  # Nagłówek

            for t in triangles:

                pts = list(t.get_points())

                # Upewniamy się, że mamy 3 punkty (na wypadek błędów w logice)
                if len(pts) == 3:
                    writer.writerow([pts[0], pts[1], pts[2]])

        print(f"Pomyślnie zapisano {len(triangles)} trójkątów do {filename}")
    except IOError as e:
        print(f"Błąd zapisu triangulacji: {e}")


def load_triangulation_from_csv(filename: str, points: PointsArray) -> list[Triangle]:
    """
    Odtwarza triangulację z pliku CSV.
    UWAGA: Wymaga przekazania listy punktów (points), aby powiązać ID z obiektami.
    """
    # Tworzymy słownik {id: Point} dla szybkiego wyszukiwania (O(1)
    triangles = []

    try:
        with open(filename, mode='r', newline='', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            next(reader, None)  # Pomijamy nagłówek

            for row in reader:
                if row:
                    try:
                        ids = tuple([int(val) for val in row])

                        triangles.append(Triangle((ids)))
                    except KeyError as e:
                        print(f"Błąd: Punkt o ID {e} nie istnieje w przekazanej liście punktów.")

        print(f"Pomyślnie wczytano {len(triangles)} trójkątów z {filename}")
        return triangles
    except FileNotFoundError:
        print(f"Plik {filename} nie istnieje.")
        return []
    except Exception as e:
        print(f"Wystąpił błąd podczas wczytywania triangulacji: {e}")
        return []