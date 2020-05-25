from Animation import Animation
from Algorithm import Algorithm
from Maze import Maze
from sys import argv
import imageio
import numpy as np
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
	Animation.animate_path(path, min_path, (255,255,51), maze, "dfs.avi")

	# BFS
	print("Building BFS...")
	path, min_path = Algorithm.breadth_first_search(maze)
	Animation.animate_path(path, min_path, (255,255,51), maze, "bfs.avi")


if __name__ == '__main__':
	main()