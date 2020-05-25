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
