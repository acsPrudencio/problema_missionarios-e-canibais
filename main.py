from collections import deque
import time

esquerda = [0, 0]
direita = [0, 0]
estadoInicial = [3, 3, 0, 0]
estadoAtual = estadoInicial


def atravessarRio(posCanoa, numCanibais, numMissionarios):
    if (numCanibais + numMissionarios > 2):
        print("Não é possivel transportar mais de duas pessoas")

    if (posCanoa == 0):
        # transportando da esquerda pra direita
        esquerda[0] -= numCanibais
        esquerda[1] -= numMissionarios
        direita[0] += numCanibais
        direita[1] += numMissionarios

        posCanoa = 1
    else:
        # transportando da direita pra esquerda
        direita[0] -= numCanibais
        direita[1] -= numMissionarios
        esquerda[0] += numCanibais
        esquerda[1] += numMissionarios
        posCanoa = 0
    # ##chegando na margem direita
    ##1.(1,1) - um missionario um canibal
    ##1.(2,0) - dois missionarios zero canibais
    ##1.(0,2) - zero missionarios dois canibais
    ##1.(1,1) - um missionario um canibal


##checa se chegamos a um estado final
def checaFinal():
    if (esquerda == [0, 0]):
        print("estado final alcançado, todo mundo atravessado")


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
    # atualizando a posição do submarino
    estadoAtual[-1] = 1 - estadoAtual[-1]
    return estadoAtual


def estadosSucessores(estado):
    estadosSucessores = []
    direcao = ""
    # i e j  quantidade de missionarios e canibais a transferir
    for (i, j) in operadores:
        # desloca canoa retorna um estado possivel atingido pela transferencia
        s = deslocaCanoa(estado[:], i, j)
        if s == None: continue
        # checa se existem mais missionarios do que canibais nas margens do rio. s[0]= canibaisEsquerda,s[1] = MissionariosEsquerda,s[2] = CanibaisDireita, etc...
        if (s[0] < s[1] and s[0] > 0) or (s[2] < s[3] and s[2] > 0): continue
        if s in visitados: continue
        if (estado[4] == 0):
            direcao = "->"
        else:
            direcao = "<-"
        # coloca o estado gerado na fronteira de estados
        estadosSucessores.append(s)
    return estadosSucessores


def obtemAdjacenteNaoVisitado(elementoAnalisar):
    l = estadosSucessores(elementoAnalisar)
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
    direcao = ""

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
                if (elementoAnalisar[4] == 0):
                    direcao = "->"
                else:
                    direcao = "<-"
                print("(" + str(abs(elementoAnalisar[0] - v[0])) + "," + str(
                    abs(elementoAnalisar[1] - v[1])) + "), " + direcao)

    else:
        print("caminho não encontrado, busca sem sucesso")
    return fronteiraEstados


def buscaLargura(estadoInicial):
    fronteiraEstados = deque()
    fronteiraEstados.append(estadoInicial)
    e = estadoInicial
    visitados = set()
    visitados.add(tuple(estadoInicial))
    num_estado = 1
    num_pai = 0
    caminhoMinimo = [e[0], e[1], e[2], e[3], e[4], num_estado, 0]
    while len(fronteiraEstados) != 0:
        elementoAnalisar = fronteiraEstados.popleft()

        # print(elementoAnalisar)
        if testeObjetivo(elementoAnalisar):
            return elementoAnalisar
        # print(elementoAnalisar)
        for s in estadosSucessores(elementoAnalisar):
            if tuple(s) not in visitados:
                visitados.add(tuple(s))
                no = [s[0], s[1], s[2], s[3], num_estado, num_pai, s[4]]
                num_estado += 1
                caminhoMinimo.append(no)
                print(no)
                fronteiraEstados.append(s)
    return None


# obtem os nós sucessores, o nó escolhido para prosseguir o algoritmo
# será aquele que mais se aproxima do objetivo, ou seja com o maior somatório de
# missionarios e canibais
def obtemMenorCusto(elementoAnalisar):
    custo = []
    l = estadosSucessores(elementoAnalisar)
    if len(l) == 0:
        return None
    i = 0
    c = 0
    for item in l:
        c = item[2] + item[3]
        if (c > i):
            custo = item
            i = c
    return custo


# função de busca em profundidade
def buscaGulosa(estadoInicial):
    fronteiraEstados.append(estadoInicial)
    direcao = ""

    while len(fronteiraEstados) != 0:
        elementoAnalisar = fronteiraEstados[len(fronteiraEstados) - 1]
        if testeObjetivo(elementoAnalisar):
            print(elementoAnalisar)
            return elementoAnalisar
        print(elementoAnalisar)
        visitados.append(elementoAnalisar)
        v = obtemMenorCusto(elementoAnalisar)
        if v == None:
            fronteiraEstados.pop()
        else:
            if v not in visitados:
                fronteiraEstados.append(v)
                if (elementoAnalisar[4] == 0):
                    direcao = "->"
                else:
                    direcao = "<-"

                print("(" + str(abs(elementoAnalisar[0] - v[0])) + "," + str(
                    abs(elementoAnalisar[1] - v[1])) + "), " + direcao)

    else:
        print("caminho não encontrado, busca sem sucesso")
    return fronteiraEstados


start = time.time()

# Exemplo de uso
estadoInicial = [3, 3, 0, 0, 0]
# estadosNivel = estadosSucessores(estadoInicial)
print(fronteiraEstados)

resultado = buscaProfundidade(estadoInicial)

if resultado is not None:
    print("Caminho encontrado:")
    for estado in resultado:
        print(estado)
else:
    print("Caminho não encontrado, busca sem sucesso")
end = time.time()
print(end - start)