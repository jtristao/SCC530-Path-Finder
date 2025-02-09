from Maze import Maze
from sys import argv
import Animation
import Algorithm
import os


def file_exists(filename):
	""" Verifica se um arquivo existe na pasta local """
	return os.path.isfile(filename)

def main():
	if len(argv) != 2:
		print("Usage:")
		print("\tpython3 {} (filename)".format(argv[0]))
		exit(0)

	filename = argv[1]

	if not file_exists(filename):
		print("Invalid filename")
		exit(0)

	maze = Maze(filename)

	# DFS
	print("Building DFS...")
	path, min_path = Algorithm.depth_first_search(maze)
	Animation.animate_path(path, min_path, (255,255,51), maze, "Videos/depth_first_search.avi")

	# BFS
	print("Building Breadth First Search...")
	path, min_path = Algorithm.breadth_first_search(maze)
	Animation.animate_path(path, min_path, (255,255,51), maze, "Videos/breadth_first_search.avi")

	# Best Search First
	print("Building Best First Search...")
	path, min_path = Algorithm.best_first_search(maze)
	Animation.animate_path(path, min_path, (255,255,51), maze, "Videos/best_first_search.avi")
	
	# A*
	print("Building A* Search...")
	path, min_path = Algorithm.a_star_search(maze)
	Animation.animate_path(path, min_path, (255,255,51), maze, "Videos/a_star_search.avi")


	# Hill Climbing*
	print("Building Hill Climbing Search...")
	path, min_path = Algorithm.hill_climbing_search(maze)
	Animation.animate_path(path, min_path, (255,255,51), maze, "Videos/hill_climbing_search.avi")


if __name__ == '__main__':
	main()