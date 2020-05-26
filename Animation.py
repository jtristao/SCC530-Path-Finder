import numpy as np
import imageio
import cv2
import os

def folder_exists(foldername):
	""" Verifica se um diretorio existe na pasta local """
	return os.path.isdir(foldername)


def make_images(path, min_path, maze, color):
	""" Percorre o labirinto de acordo com path e gera uma lista de imagens
			representando essa travessia """
	imgs = list()

	original_matrix = np.copy(maze.matrix)
	img_num = 0
	for i in range(1, len(path)):
		img_num += 1
		imgs.append(maze.draw((192,192,192)))
		maze.matrix[path[i][0], path[i][1]] = -1

	
	for i in range(1, len(min_path)):
		img_num += 1
		imgs.append(maze.draw(color))
		maze.matrix[min_path[i][0], min_path[i][1]] = -2


	maze.matrix = np.copy(original_matrix)

	return imgs

def save_images(images, folder):
	""" Salva uma lista de imagens dentro de folder """

	if not folder_exists(folder):
		os.mkdir(folder)

	image_num = 0
	for image in images:
		imageio.imwrite("{}/{:03d}.png".format(folder, image_num), image)
		image_num += 1


def make_video(images, video_name):
	""" Transforma uma lista de imagens em video """

	height, width, layers=images[0].shape

	fourcc = cv2.VideoWriter_fourcc(*'mp4v')
	video = cv2.VideoWriter(video_name, fourcc, 15,(width,height))

	for j in range(len(images)):
		video.write(images[j])

	cv2.destroyAllWindows()
	video.release()

def animate_path(path, min_path, color, maze, video_name):
	images = make_images(path, min_path, maze, color)
	make_video(images, video_name)
