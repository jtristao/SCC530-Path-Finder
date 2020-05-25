from sys import argv
import numpy as np
import imageio
import cv2
import os

def file_exists(filename):
	return os.path.isfile(filename)

def folder_exists(foldername):
	return os.path.isdir(foldername)

def draw_square(color):
	square = np.full((20,20,3), color)

	return square

def find_moves(position, matrix, maze):
	directions = [[-1,0], [1,0], [0,1], [0,-1]]
	moves = list()

	for pair in directions:
		x = pair[0] + position[0]
		y = pair[1] + position[1]
		if x >= 0 and x < maze.height and y >= 0 and y < maze.width:
			if matrix[x][y] > 0:
				moves.append([x,y])

	return moves


def read_maze(filename):
	with open(filename) as fp:
		line = fp.readline()
		height = int(line[0:2])
		width = int(line[3:5])

		maze = np.zeros((height, width))
		line_cnt = 0

		while line:
			line = fp.readline()

			for i in range(len(line)):
				if line[i] == "*":
					maze[line_cnt][i] = 1
				elif line[i] == "-":
					maze[line_cnt][i] = 0
				elif line[i] == "#":
					maze[line_cnt][i] = 2
					begin = [line_cnt, i]
				elif line[i] == "$":
					maze[line_cnt][i] = 3
					end = [line_cnt, i]

			line_cnt += 1

	return height, width, maze, begin, end

class Maze:
	def __init__(self, filename):
		info = read_maze(filename)
		self.height = info[0]
		self.width = info[1] 
		self.matrix = info[2]
		self.start = info[3]
		self.end = info[4]

	def __str__(self):
		aux = "dim = ({}, {})\n".format(self.height, self.width)
		aux += "start = {}\n".format(self.start)
		aux += "end = {}".format(self.end)

		return aux

	def draw(self):
		img = np.zeros((self.height * 20, self.width * 20, 3))

		black =	draw_square((0,0,0))
		white = draw_square((255,255,255))

		for i in range(self.height):
			for j in range(self.width):
				x = i*20
				y = j*20
				if self.matrix[i][j] == 0:
					img[x:x+20, y:y+20] = black
				elif self.matrix[i][j] == 1:
					img[x:x+20, y:y+20] = white 
				elif self.matrix[i][j] == 2:
					img[x:x+20, y:y+20] = draw_square((255,0,0))
				elif self.matrix[i][j] == 3:
					img[x:x+20, y:y+20] = draw_square((0,255,0)) 
				elif self.matrix[i][j] == -1:
					img[x:x+20, y:y+20] = draw_square((192,192,192)) 


		img = np.asarray(img, dtype="uint8")

		return img

class Algorithm():
	def depth_first_search(maze):
		matrix = np.copy(maze.matrix)
		parent = dict()
		stack = list()
		path = list()

		stack.append(maze.start)

		while stack:
			cur_pos = stack.pop()
			path.append(cur_pos)

			if cur_pos == maze.end:
				break

			moves = find_moves(cur_pos, matrix, maze)
			for move in moves:
				matrix[move[0], move[1]] = -1
				stack.append(move)
				parent[tuple(move)] = cur_pos

		return path

class Animation:
	def make_images(path, maze):
		imgs = list()

		original_matrix = np.copy(maze.matrix)
		img_num = 0
		for i in range(1, len(path)):
			img_num += 1
			imgs.append(maze.draw())
			maze.matrix[path[i][0], path[i][1]] = -1

		maze.matrix = np.copy(original_matrix)

		return imgs

	def make_video(images, video_name):
		height, width, layers=images[0].shape

		fourcc = cv2.VideoWriter_fourcc(*'mp4v')
		video = cv2.VideoWriter(video_name, fourcc, 7,(width,height))

		for j in range(len(images)):
			video.write(images[j])

		cv2.destroyAllWindows()
		video.release()

	def animate_path(path, maze, video_name):
		images = Animation.make_images(path, maze)
		Animation.make_video(images, video_name)

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
	path = Algorithm.depth_first_search(maze)
	Animation.animate_path(path, maze, "dfs.avi")

if __name__ == '__main__':
	main()