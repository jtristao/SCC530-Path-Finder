from Maze import Maze
import matplotlib.pyplot as plt
import numpy as np
import Algorithm
import Animation

def plot_result(tamanhos, result, title):
	labels = [str(name) for name in tamanhos]

	x = np.arange(len(labels))  # the label locations
	width = 0.12  # the width of the bars

	fig, ax = plt.subplots()
	offset = -2*width
	for key, value in result.items():
		ax.bar(x + offset, value, width, label=str(key))
		offset += width


	# Add some text for labels, title and custom x-axis tick labels, etc.
	ax.set_title(title)
	ax.set_ylabel('Numero de iterações')
	ax.set_xlabel('Dimensões do Labirinto')
	ax.set_xticks(x)
	ax.set_xticklabels(labels)
	ax.legend()


def main():
	tamanhos = [50, 100, 250]
	n_labirintos = 10
	space_result = dict()
	path_result = dict()
	
	algorithms = ["depth first search", "breadth first search", "best first search", "a* search", "hill climbing search"]

	for t in tamanhos:
		temp = np.zeros((5*2, n_labirintos))
		print("Dimensões:", t)
		for i in range(n_labirintos):
			print("Criando Labirinto...")
			maze = Maze(random=True, height=t, width=t)

			print("Gerando caminhos...")
			path, min_ = Algorithm.depth_first_search(maze)
			temp[0][i] = len(path)
			temp[1][i] = len(min_)

			path, min_ = Algorithm.breadth_first_search(maze)
			temp[2][i] = len(path)
			temp[3][i] = len(min_)

			path, min_ = Algorithm.best_first_search(maze)
			temp[4][i] = len(path)
			temp[5][i] = len(min_)

			path, min_ = Algorithm.a_star_search(maze)
			temp[6][i] = len(path)
			temp[7][i] = len(min_)
			
			path, min_ = Algorithm.hill_climbing_search(maze)
			temp[8][i] = len(path)
			temp[9][i] = len(min_)

		print("Calculando Médias...")

		i = 0
		for alg in algorithms:
			if alg in space_result:
				space_result[alg].append(np.mean(temp[2*i]))
				path_result[alg].append(np.mean(temp[2*i+1]))
			else:
				space_result[alg] = [np.mean(temp[2*i])]
				path_result[alg] = [np.mean(temp[2*i+1])]

			i += 1

		print()


	plot_result(tamanhos, space_result, 'Comparação por Número de Iterações')
	plot_result(tamanhos, path_result, 'Comparação por Caminho Mínimo')
	print("Numero de Iterações:", space_result)
	print("Caminho Mínimo:", path_result)
	plt.show()


if __name__ == '__main__':
	main()