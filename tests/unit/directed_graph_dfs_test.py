import numpy as np

from Projekt.utils.custom_types import PointIndex, PointsArray, Triangle, TriangleIndex
from Projekt.utils.triangle_search.directed_graph_dfs import dfs_trianglation


def test_dfs_triangulation_finds_triangle_containing_point():
	p0 = np.array([0, 0])
	p1 = np.array([6, 0])
	p2 = np.array([3, 1])
	p3 = np.array([8, 1])
	p4 = np.array([0, 4])
	p5 = np.array([2, 6])
	p6 = np.array([1, 8])
	p7 = np.array([6, 10])
	p8 = np.array([8, 12])
	p9 = np.array([7, 18])
	p10 = np.array([4, 4])
	px = np.array([7, 12])
	initial_left = np.array([-5, -5])
	initial_right = np.array([15, -5])
	initial_top = np.array([5, 25])
	points: PointsArray = np.array([
		p0, p1, p2, p3, p4, p5, p6, p7, p8, p9, p10,
		initial_left, initial_right, initial_top,
	])

	triangles: list[Triangle] = [
		(PointIndex(11), PointIndex(12), PointIndex(13)),
		(PointIndex(11), PointIndex(12), PointIndex(0)),
		(PointIndex(12), PointIndex(13), PointIndex(0)),
		(PointIndex(13), PointIndex(11), PointIndex(0)),
		(PointIndex(12), PointIndex(13), PointIndex(1)),
		(PointIndex(13), PointIndex(0), PointIndex(1)),
		(PointIndex(0), PointIndex(12), PointIndex(1)),
		(PointIndex(12), PointIndex(13), PointIndex(2)),
		(PointIndex(13), PointIndex(1), PointIndex(2)),
		(PointIndex(1), PointIndex(12), PointIndex(2)),
		(PointIndex(12), PointIndex(13), PointIndex(3)),
		(PointIndex(13), PointIndex(2), PointIndex(3)),
		(PointIndex(2), PointIndex(12), PointIndex(3)),
		(PointIndex(1), PointIndex(10), PointIndex(2)),
		(PointIndex(1), PointIndex(3), PointIndex(7)),
		(PointIndex(1), PointIndex(7), PointIndex(10)),
		(PointIndex(2), PointIndex(10), PointIndex(5)),
		(PointIndex(2), PointIndex(5), PointIndex(4)),
		(PointIndex(4), PointIndex(5), PointIndex(6)),
		(PointIndex(5), PointIndex(7), PointIndex(6)),
		(PointIndex(10), PointIndex(7), PointIndex(5)),
		(PointIndex(3), PointIndex(8), PointIndex(7)),
		(PointIndex(7), PointIndex(8), PointIndex(9)),
		(PointIndex(7), PointIndex(9), PointIndex(6)),
	]

	child_graph: list[set[TriangleIndex]] = [set() for _ in triangles]
	child_graph[0] = {TriangleIndex(1), TriangleIndex(2), TriangleIndex(3)}
	child_graph[2] = {TriangleIndex(4), TriangleIndex(5), TriangleIndex(6)}
	child_graph[4] = {TriangleIndex(7), TriangleIndex(8), TriangleIndex(9)}
	child_graph[7] = {TriangleIndex(10), TriangleIndex(11), TriangleIndex(12)}
	child_graph[1] = {TriangleIndex(13), TriangleIndex(14)}
	child_graph[3] = {TriangleIndex(15), TriangleIndex(16)}
	child_graph[5] = {TriangleIndex(17), TriangleIndex(18)}
	child_graph[6] = {TriangleIndex(19)}
	child_graph[8] = {TriangleIndex(20)}
	child_graph[9] = {TriangleIndex(21)}
	child_graph[10] = {TriangleIndex(22)}
	child_graph[11] = {TriangleIndex(22), TriangleIndex(23)}
	child_graph[12] = {TriangleIndex(23)}

	result = dfs_trianglation(
		px,
		TriangleIndex(0),
		triangles,
		child_graph,
		points,
	)

	assert result == TriangleIndex(22)
