import csv
from bitalg.Projekt.utils.classes.Point import Point
from bitalg.Projekt.utils.classes.Triangle import Triangle


# --- OBSŁUGA PUNKTÓW ---

def save_points_to_csv(points: list[Point], filename: str):
    """
    Zapisuje listę obiektów Point do pliku CSV.
    Format: id,x,y
    """
    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['id', 'x', 'y'])  # Nagłówek

            for p in points:
                # Używamy getterów z Twojej klasy Point
                writer.writerow([p.get_id(), p.get_x(), p.get_y()])
        print(f"Pomyślnie zapisano {len(points)} punktów do {filename}")
    except IOError as e:
        print(f"Błąd zapisu punktów: {e}")


def load_points_from_csv(filename: str) -> list[Point]:
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
                    p_id = int(row[0])
                    x = float(row[1])
                    y = float(row[2])
                    points.append(Point(x, y))
        print(f"Pomyślnie wczytano {len(points)} punktów z {filename}")
        return points
    except FileNotFoundError:
        print(f"Plik {filename} nie istnieje.")
        return []
    except ValueError as e:
        print(f"Błąd formatu danych w pliku CSV: {e}")
        return []


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
                    writer.writerow([pts[0].get_id(), pts[1].get_id(), pts[2].get_id()])

        print(f"Pomyślnie zapisano {len(triangles)} trójkątów do {filename}")
    except IOError as e:
        print(f"Błąd zapisu triangulacji: {e}")


def load_triangulation_from_csv(filename: str, points: list[Point]) -> list[Triangle]:
    """
    Odtwarza triangulację z pliku CSV.
    UWAGA: Wymaga przekazania listy punktów (points), aby powiązać ID z obiektami.
    """
    # Tworzymy słownik {id: Point} dla szybkiego wyszukiwania (O(1))
    points_map = {p.get_id(): p for p in points}
    triangles = []

    try:
        with open(filename, mode='r', newline='', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            next(reader, None)  # Pomijamy nagłówek

            for row in reader:
                if row:
                    try:
                        ids = [int(val) for val in row]

                        p1 = points_map[ids[0]]
                        p2 = points_map[ids[1]]
                        p3 = points_map[ids[2]]

                        triangles.append(Triangle(p1, p2, p3))
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