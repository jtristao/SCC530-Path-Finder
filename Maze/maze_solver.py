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
	print("DFS solution:", min_path)
	print("DFS travelled space:", path)
	print()
	
	# BFS
	print("Building Breadth First Search...")
	path, min_path = Algorithm.breadth_first_search(maze)
	print("BFS solution:", min_path)
	print("BFS travelled space:", path)
	print()


	# Best Search First
	print("Building Best First Search...")
	path, min_path = Algorithm.best_first_search(maze)
	print("Best-search solution:", min_path)
	print("Best-search travelled space:", path)
	print()
	
	# A*
	print("Building A* Search...")
	path, min_path = Algorithm.a_star_search(maze)
	print("A* solution:", min_path)
	print("A* travelled space:", path)
	print()

	# Hill Climbing*
	print("Building Hill Climbing Search...")
	path, min_path = Algorithm.hill_climbing_search(maze)
	print("Hill Climbing solution:", min_path)
	print("Hill travelled space:", path)
	print()



if __name__ == '__main__':
	main()