import numpy as np
import csv

from Projekt.utils.custom_types import Triangle, PointIndex, PointsArray


# --- OBSŁUGA PUNKTÓW ---

def save_points_to_csv(points: PointsArray, filename: str):
    """
    Zapisuje tablicę punktów do pliku CSV.
    Format: id,x,y
    """
    points = np.asarray(points)
    if points.ndim != 2 or points.shape[1] != 2:
        raise ValueError("Punkty muszą mieć kształt (N, 2).")

    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['id', 'x', 'y'])

            for i,p in enumerate(points):
                writer.writerow([i, p[0], p[1]])
        print(f"Pomyślnie zapisano {len(points)} punktów do {filename}")
    except IOError as e:
        print(f"Błąd zapisu punktów: {e}")


def load_points_from_csv(filename: str) -> PointsArray:
    """
    Wczytuje punkty z pliku CSV jako tablicę o kształcie (N, 2).
    """
    try:
        points_by_id = {}
        with open(filename, mode='r', newline='', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            next(reader, None)

            for row in reader:
                if not row:
                    continue
                if len(row) != 3:
                    raise ValueError("Każdy wiersz punktu musi zawierać id, x i y.")
                point_id = int(row[0])
                if point_id in points_by_id:
                    raise ValueError(f"Powtórzony identyfikator punktu: {point_id}.")
                points_by_id[point_id] = [np.float64(row[1]), np.float64(row[2])]

        expected_ids = set(range(len(points_by_id)))
        if set(points_by_id) != expected_ids:
            raise ValueError("Identyfikatory punktów muszą być kolejne i zaczynać się od 0.")

        points = np.asarray([points_by_id[index] for index in range(len(points_by_id))], dtype=float)
        print(f"Pomyślnie wczytano {len(points)} punktów z {filename}")
        return points
    except FileNotFoundError:
        print(f"Plik {filename} nie istnieje.")
        return np.empty((0, 2), dtype=float)
    except ValueError as e:
        print(f"Błąd formatu danych w pliku CSV: {e}")
        return np.empty((0, 2), dtype=float)


def save_triangulation_to_csv(triangles: list[Triangle], filename: str):
    """
    Zapisuje triangulację (listę trójkątów) do CSV.
    Zapisuje ID punktów składowych: p1_id, p2_id, p3_id
    """
    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['p1_id', 'p2_id', 'p3_id'])  # Nagłówek

            for triangle in triangles:
                if len(triangle) != 3:
                    raise ValueError("Każdy trójkąt musi zawierać trzy indeksy punktów.")
                writer.writerow([int(index) for index in triangle])

        print(f"Pomyślnie zapisano {len(triangles)} trójkątów do {filename}")
    except IOError as e:
        print(f"Błąd zapisu triangulacji: {e}")


def load_triangulation_from_csv(filename: str, points: PointsArray) -> list[Triangle]:
    """
    Wczytuje triangulację jako listę krotek indeksów punktów.
    Parametr points służy do sprawdzenia zakresu indeksów.
    """
    points = np.asarray(points)
    if points.ndim != 2 or points.shape[1] != 2:
        raise ValueError("Punkty muszą mieć kształt (N, 2).")

    triangles = []

    try:
        with open(filename, mode='r', newline='', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            next(reader, None)

            for row in reader:
                if not row:
                    continue
                if len(row) != 3:
                    raise ValueError("Każdy wiersz trójkąta musi zawierać trzy indeksy.")

                ids = tuple(PointIndex(int(value)) for value in row)
                if any(index < 0 or index >= len(points) for index in ids):
                    raise ValueError(f"Trójkąt zawiera indeks spoza zakresu: {ids}.")
                if len(set(ids)) != 3:
                    raise ValueError(f"Trójkąt nie może zawierać powtórzonego indeksu: {ids}.")
                triangles.append(ids)

        print(f"Pomyślnie wczytano {len(triangles)} trójkątów z {filename}")
        return triangles
    except FileNotFoundError:
        print(f"Plik {filename} nie istnieje.")
        return []
    except ValueError as e:
        print(f"Błąd formatu danych w pliku CSV: {e}")
        return []