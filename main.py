canibais = {'esquerda':0,
                'direita':0}
missionarios = {'esquerda':0,
                'direita':0}
    

estadoInicial = [3,3,0,0]
estadoAtual = estadoInicial


def atravessarRio(posCanoa,numCanibais,numMissionarios):
    if(numCanibais+numMissionarios>2):
        print("Não é possivel transportar mais de duas pessoas")

    if(posCanoa==0):
        canibais['direita']+=numCanibais
        missionarios['direita']+=numMissionarios
    ##chegando na margem direita
    ##1.(1,1) - um missionario um canibal
    ##1.(2,0) - dois missionarios zero canibais
    ##1.(0,2) - zero missionarios dois canibais
    ##1.(1,1) - um missionario um canibal

##checa se chegamos a um estado final
def checaFinal():
    if(canibais['esquerda']==0 and missionarios['esquerda']==0):
        print("estado final alcançado, todo mundo atravessado")