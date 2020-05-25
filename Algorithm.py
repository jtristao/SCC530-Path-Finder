import numpy as np

class Algorithm():
	""" Implementa os algoritmos """

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

	def __bfs_min_path(parent, begin, end):
		min_path = list()
		cur_pos = tuple(begin)

		while cur_pos != end:
			min_path.append(cur_pos)
			cur_pos = parent[tuple(cur_pos)]

		min_path.append(end)

		return min_path


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

		min_path = Algorithm.__bfs_min_path(parent, maze.end, maze.start)

		return path, min_path