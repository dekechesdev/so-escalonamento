import random

MAXIMO_TEMPO_EXECUCAO = 65535

n_processos = 4 #qnts processos existem

def main():
    tempo_execucao = [0] * n_processos  #qnt tempo de CPU o processo precisa
    tempo_chegada = [0] * n_processos
    prioridade = [0] * n_processos
    tempo_espera = [0] * n_processos
    tempo_restante = [0] * n_processos
    tempo_termino = [0] * n_processos

    popular_processos(tempo_execucao, tempo_espera, tempo_restante, tempo_chegada, prioridade)

    imprime_processos(tempo_execucao, tempo_espera, tempo_restante, tempo_chegada, prioridade)

    # Escolher algoritmo
    while True:
        alg = int(input(
            "Escolha o algoritmo? \n[1=FCFS / 2=SJF /  3=SJF Preemptivo / 4=Prioridade / 5=Prioridade Preemptivo / 9=Sair]: "))

        if alg == 1:  # FCFS
            FCFS(tempo_execucao, tempo_espera, tempo_restante, tempo_chegada)

        if alg == 2:
            SJFS(tempo_execucao, tempo_espera, tempo_restante, tempo_chegada)

        if alg == 3:
            SJFS_P(tempo_execucao, tempo_espera, tempo_restante, tempo_chegada, tempo_termino)

        if alg == 4:
            Prioridade(tempo_execucao, tempo_espera, tempo_restante, tempo_chegada, prioridade)

        if alg == 5:
            Prioridade_P(tempo_execucao, tempo_espera, tempo_restante, tempo_chegada, tempo_termino, prioridade)
        elif alg == 9:
            break

def popular_processos(tempo_execucao, tempo_espera, tempo_restante, tempo_chegada, prioridade):
    aleatorio = int(input("Sera aleatorio?:  "))

    for i in range(n_processos):
        # Popular Processos Aleatorio
        if aleatorio == 1:  # input inicial, gera valores aleatorios para exemplo
            tempo_execucao[i] = random.randint(1, 10)
            tempo_chegada[i] = random.randint(1, 10)
            prioridade[i] = random.randint(1, 15)
        # Popular Processos Manual
        else:
            tempo_execucao[i] = int(input("Digite o tempo de execucao do processo[" + str(i) + "]:  "))
            tempo_chegada[i] = int(input("Digite o tempo de chegada do processo[" + str(i) + "]:  "))
            prioridade[i] = int(input("Digite a prioridade do processo[" + str(i) + "]:  "))

        tempo_restante[i] = tempo_execucao[i]
        tempo_espera[i] = 0


def imprime_processos(tempo_execucao, tempo_espera, tempo_restante, tempo_chegada, prioridade):
    # Imprime lista de processos
    for i in range(n_processos):
        print("Processo[" + str(i) + "]: tempo_execucao=" + str(tempo_execucao[i]) +
              " tempo_restante=" + str(tempo_restante[i]) +
              " tempo_chegada=" + str(tempo_chegada[i]) +
              " prioridade =" + str(prioridade[i]))

def imprime_stats(espera):
    tempo_espera = list(espera)
    # Implementar o calculo e impressao de estatisticas

    tempo_espera_total = 0.0

    for i in range(n_processos):
        print("Processo[" + str(i) + "]: tempo_espera=" + str(tempo_espera[i]))
        tempo_espera_total = tempo_espera_total + tempo_espera[i]

    print("Tempo medio de espera: " + str(tempo_espera_total / n_processos))


def FCFS(execucao, espera, restante, tempo_chegada):
    tempo_execucao = list(execucao) #cria lista dos parametros pra poder usar
    tempo_espera = list(espera)
    tempo_restante = list(restante)
    #chegada é a ordem dos indices

    processo_em_execucao = 0

    for i in range(1, MAXIMO_TEMPO_EXECUCAO):
        print("tempo[" + str(i) + "]: processo[" + str(processo_em_execucao) + "] restante=" +
              str(tempo_restante[processo_em_execucao]))

        if tempo_execucao[processo_em_execucao] == tempo_restante[processo_em_execucao]:
            tempo_espera[processo_em_execucao] = i - 1

        if tempo_restante[processo_em_execucao] == 1:
            if processo_em_execucao == (n_processos - 1):
                break
            else:
                processo_em_execucao = processo_em_execucao + 1
        else:
            tempo_restante[processo_em_execucao] = tempo_restante[processo_em_execucao] - 1

    imprime_stats(tempo_espera)

def SJFS(execucao, espera, restante, chegada):
    tempo_execucao = list(execucao)
    tempo_espera = list(espera)
    tempo_restante = list(restante)
    tempo_chegada = list(chegada)

    processo_em_execucao = -1
    contador = 0

    for volta in range(0, MAXIMO_TEMPO_EXECUCAO):
        if processo_em_execucao == -1:
            processo_menor_tempo = -1
            for processo in range(n_processos):
                if tempo_chegada[processo] <= volta and tempo_restante[processo] > 0:
                    if processo_menor_tempo == -1 or tempo_execucao[processo] < tempo_execucao[processo_menor_tempo] or (tempo_execucao[processo] == tempo_execucao[processo_menor_tempo] and tempo_chegada[processo_menor_tempo] > tempo_chegada[processo]):
                        processo_menor_tempo = processo #processo atual vira o de menor tempo
            if processo_menor_tempo != -1:
                processo_em_execucao = processo_menor_tempo
                tempo_espera[processo_em_execucao] = volta - tempo_chegada[processo_em_execucao]
        print("tempo[" + str(volta) + "]: processo[" + str(processo_em_execucao) + "] restante=" + str(tempo_restante[processo_em_execucao]))
        if processo_menor_tempo != -1:
            tempo_restante[processo_em_execucao] -= 1
            if tempo_restante[processo_em_execucao] == 0:
                processo_em_execucao = -1
                contador += 1
                if contador == n_processos:
                    break

    imprime_stats(tempo_espera)

def SJFS_P(execucao, espera, restante, chegada, termino):
    tempo_execucao = list(execucao)
    tempo_espera = list(espera)
    tempo_restante = list(restante)
    tempo_chegada = list(chegada)
    lista_termino = list(termino)

    processo_em_execucao = -1
    contador = 0

    for volta in range(0, MAXIMO_TEMPO_EXECUCAO):
        processo_menor_tempo = -1
        for processo in range(n_processos):
            if tempo_chegada[processo] <= volta and tempo_restante[processo] > 0:
                if processo_menor_tempo == -1 or tempo_restante[processo] < tempo_restante[processo_menor_tempo] or (tempo_restante[processo] == tempo_restante[processo_menor_tempo] and tempo_chegada[processo_menor_tempo] > tempo_chegada[processo]):
                    processo_menor_tempo = processo #processo atual vira o de menor tempo
        if processo_menor_tempo != -1:
            processo_em_execucao = processo_menor_tempo
        print("tempo[" + str(volta) + "]: processo[" + str(processo_em_execucao) + "] restante=" + str(tempo_restante[processo_em_execucao]))
        if processo_menor_tempo != -1:
            tempo_restante[processo_em_execucao] -= 1
            if tempo_restante[processo_em_execucao] == 0:
                lista_termino[processo_em_execucao] = volta + 1
                contador += 1
                if contador == n_processos:
                    break
    for x in range(n_processos):
        tempo_espera[x] = lista_termino[x] - tempo_chegada[x] - tempo_execucao[x]

    imprime_stats(tempo_espera)

def Prioridade(execucao, espera, restante, chegada, prioridade):
    tempo_execucao = list(execucao)
    tempo_espera = list(espera)
    tempo_restante = list(restante)
    tempo_chegada = list(chegada)
    valor_prioridade = list(prioridade)

    #menor valor maior prioridade

    processo_em_execucao = -1
    contador = 0

    for volta in range(0, MAXIMO_TEMPO_EXECUCAO):
        if processo_em_execucao == -1:
            processo_menor_tempo = -1
            for processo in range(n_processos):
                if tempo_chegada[processo] <= volta and tempo_restante[processo] > 0:
                    if processo_menor_tempo == -1 or valor_prioridade[processo] < valor_prioridade[processo_menor_tempo] or (valor_prioridade[processo] == valor_prioridade[processo_menor_tempo] and tempo_chegada[processo_menor_tempo] > tempo_chegada[processo]):
                        processo_menor_tempo = processo #processo atual vira o de menor tempo
            if processo_menor_tempo != -1:
                processo_em_execucao = processo_menor_tempo
                tempo_espera[processo_em_execucao] = volta - tempo_chegada[processo_em_execucao]
        print("tempo[" + str(volta) + "]: processo[" + str(processo_em_execucao) + "] restante=" + str(tempo_restante[processo_em_execucao]))
        if processo_menor_tempo != -1:
            tempo_restante[processo_em_execucao] -= 1
            if tempo_restante[processo_em_execucao] == 0:
                processo_em_execucao = -1
                contador += 1
                if contador == n_processos:
                    break
    imprime_stats(tempo_espera)

def Prioridade_P(execucao, espera, restante, chegada, termino, prioridade):
    tempo_execucao = list(execucao)
    tempo_espera = list(espera)
    tempo_restante = list(restante)
    tempo_chegada = list(chegada)
    lista_termino = list(termino)
    valor_prioridade = list(prioridade)

    processo_em_execucao = -1
    contador = 0

    for volta in range(0, MAXIMO_TEMPO_EXECUCAO):
        processo_menor_tempo = -1
        for processo in range(n_processos):
            if tempo_chegada[processo] <= volta and tempo_restante[processo] > 0:
                if processo_menor_tempo == -1 or valor_prioridade[processo] < valor_prioridade[processo_menor_tempo] or (valor_prioridade[processo] == valor_prioridade[processo_menor_tempo] and tempo_chegada[processo_menor_tempo] > tempo_chegada[processo]):
                    processo_menor_tempo = processo #processo atual vira o de menor tempo
        if processo_menor_tempo != -1:
            processo_em_execucao = processo_menor_tempo
        print("tempo[" + str(volta) + "]: processo[" + str(processo_em_execucao) + "] restante=" + str(tempo_restante[processo_em_execucao]))
        if processo_menor_tempo != -1:
            tempo_restante[processo_em_execucao] -= 1
            if tempo_restante[processo_em_execucao] == 0:
                lista_termino[processo_em_execucao] = volta + 1
                contador += 1
                if contador == n_processos:
                    break
    for x in range(n_processos):
        tempo_espera[x] = lista_termino[x] - tempo_chegada[x] - tempo_execucao[x]

    imprime_stats(tempo_espera)

main()