import numpy as np

def read_maze(filename):
	""" Le um arquivo e retorna as informacoes da matriz """

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
					maze[line_cnt][i] = 1
					begin = [line_cnt, i]
				elif line[i] == "$":
					maze[line_cnt][i] = 1
					end = [line_cnt, i]

			line_cnt += 1

	return height, width, maze, begin, end

def draw_square(color):
	""" Cria uma matriz de 20*20*3 com a cor definida """
	square = np.full((20,20,3), color)

	return square


class Maze:
	""" Guarda as informacoes do labirinto """
	def __init__(self, filename=None, random=False, height=-1, width=-1, start=[-1,-1], end=[-1,-1]):
		if random:
			self.height = height
			self.width = width 
			self.matrix = Maze.random_maze(height, width, tuple(start))
			self.start = start
			self.end = end
		else if filename:
			info = read_maze(filename)
			self.height = info[0]
			self.width = info[1] 
			self.matrix = info[2]
			self.start = info[3]
			self.end = info[4]
		else:
			print("Invalid Arguments Building Maze.")


	def __str__(self):
		aux = "dim = ({}, {})\n".format(self.height, self.width)
		aux += "start = {}\n".format(self.start)
		aux += "end = {}".format(self.end)

		return aux

	def find_moves(self, position, matrix):
		""" Dada uma posicao inicial, retorna uma lista de movimentos possiveis """

		directions = [[-1,0], [1,0], [0,1], [0,-1]]
		moves = list()

		for pair in directions:
			x = pair[0] + position[0]
			y = pair[1] + position[1]
			if x >= 0 and x < self.height and y >= 0 and y < self.width:
				if matrix[x][y] > 0:
					moves.append([x,y])

		return moves

	def draw(self, color):
		""" Transforma o labirinto em uma imagem """

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
				elif self.matrix[i][j] == -1:
					img[x:x+20, y:y+20] = draw_square((192,192,192))
				elif self.matrix[i][j] == -2:
					img[x:x+20, y:y+20] = draw_square(color)

		# Desenha posicao inicial
		x = self.start[0]*20
		y = self.start[1]*20
		img[x:x+20, y:y+20] = draw_square((255,0,0))
		
		# Desenha a posicao final
		x = self.end[0]*20
		y = self.end[1]*20
		img[x:x+20, y:y+20] = draw_square((0,255,0))

		img = np.asarray(img, dtype="uint8")

		return img

	def random_maze(height, width, start):
		maze = [[0 for x in range(height)] for y in range(width)]
		dx = [0, 1, 0, -1]
		dy = [-1, 0, 1, 0] # 4 directions to move in the maze

		# start the maze from a random cell
		stack = [start]

		while len(stack) > 0:
			(x, y) = stack[-1]
			maze[y][x] = 1
			# find a new cell to add
			neighbours_list = [] # list of available neighbors
			for i in range(4):
				neighbor_x = x + dx[i]
				neighbor_y = y + dy[i]
				if neighbor_x >= 0 and neighbor_x < height and neighbor_y >= 0 and neighbor_y < width:
					if maze[neighbor_y][neighbor_x] == 0:
						# of occupied neighbors must be 1
						ctr = 0
						for j in range(4):
							ex = neighbor_x + dx[j]
							ey = neighbor_y + dy[j]
							if ex >= 0 and ex < height and ey >= 0 and ey < width:
								if maze[ey][ex] == 1: 
									ctr += 1
									if ctr == 1: 
										neighbours_list.append(i)

			# if 1 or more neighbors available then randomly select one and move
			if len(neighbours_list) > 0:
				ir = neighbours_list[random.randint(0, len(neighbours_list) - 1)]
				x += dx[ir]
				y += dy[ir]
				stack.append((x, y))
			else: 
				stack.pop()

		return maze
