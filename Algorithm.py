import numpy as np
import heapq

def find_distance(coord, maze, heuristic):
	if heuristic == "euclidean":
		return ((coord[0] - maze.end[0])**2 + (coord[1] - maze.end[1])**2)**0.5
	else:
		return abs(coord[0] - maze.end[0]) + abs(coord[1] - maze.end[1])

def __min_path(parent, begin, end):
	min_path = list()
	cur_pos = tuple(begin)

	while cur_pos != end:
		min_path.append(cur_pos)
		cur_pos = parent[tuple(cur_pos)]

	min_path.append(end)

	return min_path

def depth_first_search(maze):
	matrix = np.copy(maze.matrix)
	stack = list()
	path = list()

	stack.append(maze.start)

	while stack:
		cur_pos = stack.pop()
		path.append(cur_pos)

		if cur_pos == maze.end:
			break

		moves = maze.find_moves(cur_pos, matrix)
		for move in moves:
			matrix[move[0], move[1]] = -1
			stack.append(move)

	return path, path[::-1]

def breadth_first_search(maze):
	matrix = np.copy(maze.matrix)
	parent = dict()
	queue = list()
	path = list()

	queue.append(maze.start)

	while queue:
		cur_pos = queue.pop(0)
		path.append(cur_pos)

		if cur_pos == maze.end:
			break

		moves = maze.find_moves(cur_pos, matrix)
		for move in moves:
			matrix[move[0], move[1]] = -1
			queue.append(move)
			parent[tuple(move)] = cur_pos

	min_path = __min_path(parent, maze.end, maze.start)

	return path, min_path

def best_first_search(maze, heuristic="euclidean"):
	matrix = np.copy(maze.matrix)

	path = list()
	parent = dict()
	heap = [(0, maze.start[0], maze.start[1])]
	heapq.heapify(heap)


	while heap:
		cur_pos = heapq.heappop(heap)
		val = cur_pos[0]
		coord = [cur_pos[1], cur_pos[2]]

		path.append(coord)

		if coord == maze.end:
			break

		moves = maze.find_moves(coord, matrix)
		for move in moves:
			matrix[coord[0], coord[1]] = -1
			distance = find_distance(move, maze, heuristic)
			heapq.heappush(heap, (distance, move[0], move[1]))
			parent[tuple(move)] = coord

	min_path = __min_path(parent, maze.end, maze.start)

	return path, min_path

def a_star_search(maze, heuristic="euclidean"):
	matrix = np.copy(maze.matrix)

	path = list()
	parent = dict()
	# Tupla(peso, distancia, coord_x, coord_y)
	heap = [(0, 0, maze.start[0], maze.start[1])]
	heapq.heapify(heap)


	while heap:
		cur_pos = heapq.heappop(heap)
		val = cur_pos[0]
		height = cur_pos[1]
		coord = [cur_pos[2], cur_pos[3]]

		path.append(coord)

		if coord == maze.end:
			break

		moves = maze.find_moves(coord, matrix)
		for move in moves:
			matrix[coord[0], coord[1]] = -1

			distance = find_distance(move, maze, heuristic) + height + 1

			heapq.heappush(heap, (distance, height+1, move[0], move[1]))
			parent[tuple(move)] = coord

	min_path = __min_path(parent, maze.end, maze.start)

	return path, min_path

def hill_climbing_search(maze, heuristic="euclidean"):
	matrix = np.copy(maze.matrix)
	stack = list()
	path = list()
	parent = dict()

	stack.append(maze.start)

	while stack:
		cur_pos = stack.pop()
		path.append(cur_pos)

		if cur_pos == maze.end:
			break

		moves = maze.find_moves(cur_pos, matrix)
		
		weights = list()
		for move in moves:
			weights.append(find_distance(move, maze, heuristic))

		pairs = list(zip(moves, weights))
		pairs = sorted(pairs, key=lambda x: x[1], reverse=True)
		for coord, weight in pairs:
			matrix[coord[0], coord[1]] = -1
			stack.append(coord)
			parent[tuple(coord)] = cur_pos

	min_path = __min_path(parent, maze.end, maze.start)

	return path, min_path