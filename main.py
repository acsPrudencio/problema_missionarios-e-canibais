from collections import deque
import heapq

# transportando da esquerda pra direita

# chegando na margem direita
# 1.(1,1) - um missionario um canibal
# 1.(2,0) - dois missionarios zero canibais
# 1.(0,2) - zero missionarios dois canibais
# 1.(1,1) - um missionario um canibal
#
# checa se chegamos a um estado final

# 0-missionarioEsquerda
# 1-CanibaisEsquerda
# 2-MissionarioDireita
# 3-CanibaisDireita


estadoInicial = [3, 3, 0, 0, 0]
estadoAtual = estadoInicial
# combinações possiveis de estados e canibais
operadores = [(1, 0), (1, 1), (2, 0), (0, 2)]

fronteiraEstados = []
visitados = []


def deslocaCanoa(estadoAtual, nummissionarios=0, numcanibais=0):
    if nummissionarios + numcanibais > 2:
        print("nao eh possivel transposrtar mais de duas pessoas.")

    moveCanoa = False
    if estadoAtual[-1] == 0:
        missionariosOrigem = 0
        canibaisOrigem = 1
        missionariosDestino = 2
        canibaisDestino = 3

    else:
        missionariosOrigem = 2
        canibaisOrigem = 3
        missionariosDestino = 0
        canibaisDestino = 1

    if estadoAtual[missionariosOrigem] == 0 and estadoAtual[canibaisOrigem] == 0:
        return

    # atualizando a posição da canoa

    for i in range(min(nummissionarios, estadoAtual[missionariosOrigem])):
        estadoAtual[missionariosOrigem] -= 1
        estadoAtual[missionariosDestino] += 1
        moveCanoa = True

    # transportando os canibais

    for i in range(min(numcanibais, estadoAtual[canibaisOrigem])):
        estadoAtual[canibaisOrigem] -= 1
        estadoAtual[canibaisDestino] += 1
        moveCanoa = True
    if (not moveCanoa):
        return

    estadoAtual[-1] = 1 - estadoAtual[-1]
    return estadoAtual


def estadosSucessores(estado):
    estadosSucessores = []
    # i e j  quantidade de missionarios e canibais a transferir
    for (i, j) in operadores:
        # desloca canoa retorna um estado possivel atingido pela transferencia

        s = deslocaCanoa(estado[:], i, j)
        # s = deslocaCanoa(estado[:],i,j)
        if s == None: continue
        # checa se existem mais missionarios do que canibais nas margens do rio. s[0]= canibaisEsquerda,s[1] = MissionariosEsquerda,s[2] = CanibaisDireita, etc...
        if (s[0] < s[1] and s[0] > 0) or (s[2] < s[3] and s[2] > 0): continue
        if s in visitados: continue
        # coloca o estado gerado na fronteira de estados
        estadosSucessores.append(s)
    return estadosSucessores


def obtemAdjacenteNaoVisitado(elementoAnalisar):
    l = estadosSucessores(elementoAnalisar[:])  # Correção: use elementoAnalisar[:]
    if len(l) > 0:
        return l[0]
    else:
        return None


# testa se chegamos a um estado final do programa. Estado com canibais e missionários no lado direito
def testeObjetivo(estado):
    if estado[2] >= 3 and estado[3] >= 3:
        return True
    else:
        return False


# função de busca em profundidade
def buscaProfundidade(estadoInicial):
    fronteiraEstados.append(estadoInicial)
    while len(fronteiraEstados) != 0:
        elementoAnalisar = fronteiraEstados[len(fronteiraEstados) - 1]
        if testeObjetivo(elementoAnalisar):
            return elementoAnalisar
        print(elementoAnalisar)
        visitados.append(elementoAnalisar)
        v = obtemAdjacenteNaoVisitado(elementoAnalisar)
        if v == None:
            fronteiraEstados.pop()
        else:
            if v not in visitados:
                fronteiraEstados.append(v)
    else:
        print("caminho não encontrado, busca sem sucesso")
    return fronteiraEstados


def buscaLargura(estadoInicial):
    fronteiraEstados = deque()
    fronteiraEstados.append(estadoInicial)
    visitados = set()
    visitados.add(tuple(estadoInicial))

    while len(fronteiraEstados) != 0:
        elementoAnalisar = fronteiraEstados.popleft()
        print(elementoAnalisar)
        if testeObjetivo(elementoAnalisar):
            return elementoAnalisar
        print(elementoAnalisar)
        for s in estadosSucessores(elementoAnalisar):
            if tuple(s) not in visitados:
                visitados.add(tuple(s))
                fronteiraEstados.append(s)

    return None


# obtem os nós sucessores, e entre eles o de menor custo

def obtemMenorCusto(elementoAnalisar):
    custo = {}
    l = estadosSucessores(elementoAnalisar)
    if len(l) == 0:
        return None
    i = 0
    for c in l:
        custo[c] = (c, (c[0] + c[1]) / 2)

    return min(custo)


# Retorna a estimativa do custo que resta (h(n)) pra alcançar o objetivo a partir do estado

def heuristicaAestrela(estado):
    numMissionariosEsquerda = estado[0]
    numCanibaisEsquerda = estado[1]
    return numMissionariosEsquerda + numCanibaisEsquerda


# função de busca em profundidade
def buscaGulosa(estadoInicial):
    fronteiraEstados.append(estadoInicial)
    while len(fronteiraEstados) != 0:
        elementoAnalisar = fronteiraEstados[len(fronteiraEstados) - 1]
        if testeObjetivo(elementoAnalisar):
            return elementoAnalisar
        print(elementoAnalisar)
        visitados.append(elementoAnalisar)
        v = obtemMenorCusto(elementoAnalisar)
        if v == None:
            fronteiraEstados.pop()
        else:
            if v not in visitados:
                fronteiraEstados.append(v)
    else:
        print("caminho não encontrado, busca sem sucesso")
    return fronteiraEstados


def buscaAestrela(estadoInicial):
    fronteiraEstados = []
    heapq.heappush(fronteiraEstados, ([0, estadoInicial]))
    visitados = []
    while len(fronteiraEstados) != 0:
        elementoAnalisar = heapq.heappop(fronteiraEstados)
    if testeObjetivo(elementoAnalisar):
        return elementoAnalisar
    visitados.append(elementoAnalisar)
    for s in estadosSucessores(elementoAnalisar):
        if s in visitados:
            continue
        g = elementoAnalisar[4] + 1  # custo ja percorrido + custo da ação atual
        h = heuristicaAestrela(s)  # heuristica para o estado s
        f = g + h  # custo total = custo ja percorrido + estimativa do custo que resta
        heapq.heappush(fronteiraEstados, (f, s))
    return None


# Exemplo de uso
estadoInicial = [3, 3, 0, 0, 0]
# estadosNivel = estadosSucessores(estadoInicial)
print(fronteiraEstados)

resultado = buscaGulosa(estadoInicial)

if resultado is not None:
    print("Caminho encontrado:")
    for estado in resultado:
        print(estado)
else:
    print("Caminho não encontrado, busca sem sucesso")

# resultadoestrela = buscaAestrela(estadoInicial)

# if resultadoestrela is not None:
#    print("Caminho encontrado:")
#    print(resultadoestrela)  # Imprime o estado diretamente
# else:
#    print("Caminho não encontrado, busca sem sucesso")