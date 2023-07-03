# from graphviz import Graph
class Vertice:
	def __init__(self,rotulo):
		self.rotulo = rotulo
	def __eq__(self,outro):
		return outro.rotulo == self.rotulo
	def __repr__(self):
		return self.rotulo
	def __hash__(self):
		return hash(self.rotulo)


class Grafo:
	def __init__(self):
		self.listaAdjacencias = dict()
		self.listaVertices = set()

	def adicionaVertice(self, rotulo):
		self.listaVertices.add(Vertice(rotulo))

	def localizaRotulo(self, rotulo):
		for i in self.listaVertices:
			if i.rotulo == rotulo:
				return i
			return -1

	def adicionaArco(self, r1, r2):
		if not self.listaAdjacencias.get(r1):
			self.listaAdjacencias[r1] = [r2]
		else:
			self.listaAdjacencias[r1].append(r2)

		if not self.listaAdjacencias.get(r2):
			self.listaAdjacencias[r2] = [r1]
		else:
			self.listaAdjacencias[r2].append(r1)

	# transforma o grafo em uma string
	def __repr__(self):
		return str(self.listaAdjacencias)

	# def desenhaGrafo(self):
	# 	g = Graph(comment='Nome grafo', strict=True)
	# 	for i in self.listaVertices:
	# 		g.node(i.rotulo, i.rotulo, fontsize="10")
	# 	for k, v in self.listaAdjacencias.items():
	# 		for j in v:
	# 			g.edge(k, j, dir="none")
	# 	return g

def main():
 x = Vertice("Teste")
 print(x)

if __name__ == '__main__':
    main()