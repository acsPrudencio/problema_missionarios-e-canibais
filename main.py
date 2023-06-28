from collections import deque

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


estadoInicial = [3, 3, 0, 0, 0]
estadoAtual = estadoInicial
# combinações possiveis de estados e canibais
operadores = [(1, 0), (1, 1), (2, 0), (0, 2)]

borda = []
visitados = []


def deslocaCanoa(estadoAtual, nummissionarios=0, numcanibais=0):
    if nummissionarios + numcanibais > 2:
        print("nao eh possivel transposrtar mais de duas pessoas.")

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

    # atualizando a posição do submarino
    estadoAtual[-1] = 1 - estadoAtual[-1]

    for i in range(min(nummissionarios, estadoAtual[missionariosOrigem])):
        estadoAtual[missionariosOrigem] -= 1
        estadoAtual[canibaisDestino] -= 1

    # transportando os canibais

    for i in range(min(numcanibais, estadoAtual[canibaisOrigem])):
        estadoAtual[canibaisOrigem] -= 1
        estadoAtual[canibaisDestino] -= 1

    return estadoAtual


def sucessores(estado):
    sucessores = []
    # i e j quantidade de missionarios e canibais a transferir
    for (i, j) in operadores:
        # desloca canoa retorna um estado possivel atingido pela transferencia

        s = deslocaCanoa(estado[:], i, j)
        if s == None: continue
        if (s[0] < s[1] and s[0] > 0) or (s[2] < s[3] and s[2] > 0): continue
        if s in visitados: continue
        # coloca o estado gerado na fronteira de estados
        sucessores.append(s)
    return sucessores


def obtemAdjacenteNaoVisitado(elementoAnalisar):
    l = sucessores(elementoAnalisar)
    if len(l) > 0:
        return l[0]
    else:
        return -l


# testa se chegamos a um estado final do programa. Estado com canibais e missionários no lado direito
def testeMeta(estado):
    if estado[2] >= 3 and estado[3] >= 3:
        return True
    else:
        return False


# função de busca em profundidade
def dfs(estadoInicial):
    borda.append(estadoInicial)
    while len(borda) != 0:
        elementoAnalisar = borda[len(borda) - 1]
        if testeMeta(elementoAnalisar): break
        v = obtemAdjacenteNaoVisitado(elementoAnalisar)
        if v == -1:
            borda.pop()
        else:
            visitados.append(v)
            borda.append(v)
    else:
        print("caminho não encontrado, busca sem sucesso")
    return borda


def bfs(estadoInicial):
    borda = deque()
    borda.append(estadoInicial)
    visitados = set()
    visitados.add(tuple(estadoInicial))

    while len(borda) != 0:
        elementoAnalisar = borda.popleft()

        if testeMeta(elementoAnalisar):
            return elementoAnalisar

        for s in sucessores(elementoAnalisar):
            if tuple(s) not in visitados:
                visitados.add(tuple(s))
                borda.append(s)

    return None


# Exemplo de uso
estadoInicial = [3, 3, 0, 0, 0]
resultado = bfs(estadoInicial)

if resultado is not None:
    print("Caminho encontrado:")
    for estado in resultado:
        print(estado)
else:
    print("Caminho não encontrado, busca sem sucesso")