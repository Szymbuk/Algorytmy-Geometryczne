import numpy as np

from Projekt.utils.csvIO import (
    load_points_from_csv,
    load_triangulation_from_csv,
    save_points_to_csv,
    save_triangulation_to_csv,
)


def test_points_and_triangles_round_trip(tmp_path):
    points = np.array([[1.5, -2.0], [3.25, 4.0], [-5.0, 0.75]])
    triangles = [(0, 1, 2)]
    points_path = tmp_path / "points.csv"
    triangles_path = tmp_path / "triangles.csv"

    save_points_to_csv(points, str(points_path))
    save_triangulation_to_csv(triangles, str(triangles_path))

    loaded_points = load_points_from_csv(str(points_path))
    loaded_triangles = load_triangulation_from_csv(str(triangles_path), loaded_points)

    np.testing.assert_array_equal(loaded_points, points)
    assert loaded_triangles == triangles