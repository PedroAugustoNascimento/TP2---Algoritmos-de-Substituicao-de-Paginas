def otimo(vetor):
    pageMiss = 0
    molduras = []  
    numMolduras = int(vetor[1])  # numero total de molduras disponiveis
    numerosFuturos = []  # pega as páginas futuras

    # preenche a lista de numeros futuros
    for i, linha in enumerate(vetor):
        if (i > 2):  # n-3
            valores = linha.strip().split()  
            if (len(valores) >= 3): 
                numerosFuturos.append(valores[0])

    # iterando sobre páginas futuras
    for i, pagina in enumerate(numerosFuturos):
        if (pagina not in molduras):  # se a página não está na moldura atual
            pageMiss += 1  # adiciona um pageMiss
            if (len(molduras) < numMolduras):  # se ainda tiver o espaço (n=1)
                molduras.append(pagina)  # preenche a moldura
            else:
                # usa as páginas futuras
                pagina_substituir = -1
                indice_futuro = -1

                for j, p in enumerate(molduras):
                    try:
                        # procura a próxima página
                        proximo_uso = numerosFuturos[i+1:].index(p)
                    except ValueError:
                        # se não for usada, ela é substituida
                        pagina_substituir = j
                        break
                    #se a distacia do entre proximo uso for maior que o indice atual 
                    if (proximo_uso > indice_futuro):
                        indice_futuro = proximo_uso #indice é atualizado para o proximo uso
                        pagina_substituir = j # a pagina substituida atribui o valor do numero futuro atual

                # substitui a página mais distante
                molduras[pagina_substituir] = pagina
    print(pageMiss)
    return pageMiss

def nru(vetor):
    pageMiss = 0
    valores = []
    molduras = int(vetor[1])  # número de molduras
    matriz = [[-1, 0, 0, 0] for _ in range(molduras)]  # matriz com 4 colunas por padrão e as linhas são o número de molduras
    clock = int(vetor[2])  # tempo em que o bit R vai zerar

    for i, linha in enumerate(vetor):
        if i > 2:  # n-3
            valores = linha.strip().split()
            pagina = int(valores[0])  # 0
            tempo = int(valores[1])  # 0 -> tempo em que a página vai chegar

            if i == 3:  # na primeira passagem preencho a primeira linha com o primeiro valor e contabilizo um pageMiss
                matriz[0][0] = pagina
                matriz[0][1] = tempo
                matriz[0][2] = 1  # bit R -> página acessada recentemente
                matriz[0][3] = 0  # bit M -> página modificada
                pageMiss += 1
            else:
                # verifica se a página já está na memória
                pagina_na_memoria = False
                for moldura in matriz:
                    # se a página tiver na memória, atualiza somente o tempo de clock e o bit M para modificado
                    if moldura[0] == pagina:
                        pagina_na_memoria = True
                        moldura[1] = tempo  # atualiza o tempo de acesso
                        moldura[2] = 1  # seta o bit R (página acessada)
                        moldura[3] = 1  # seta o bit M para 1 (página modificada)
                        break

                if not pagina_na_memoria:
                    # se a página não está na memória incrementa o pageMiss
                    pageMiss += 1

                    # procura um caso de classe 1: bit R=0 e bit M=0
                    substituida = False
                    for moldura in matriz:
                        if moldura[2] == 0 and moldura[3] == 0:
                            # substituição de página e alteração dos demais campos (tempo, bit R e bit M)
                            moldura[0] = pagina
                            moldura[1] = tempo
                            moldura[2] = 1
                            moldura[3] = 0
                            substituida = True
                            break

                    # procura um caso classe 2: bit R=0 e bit M=1
                    if not substituida:
                        for moldura in matriz:
                            if moldura[2] == 0 and moldura[3] == 1:
                                moldura[0] = pagina
                                moldura[1] = tempo
                                moldura[2] = 1  # seta o bit R para mais acessado recentemente
                                moldura[3] = 0  # modificado volta para 0
                                substituida = True
                                break

                    # procura um caso classe 3: bit R=1 e bit M=0
                    if not substituida:
                        for moldura in matriz:
                            if moldura[2] == 1 and moldura[3] == 0:
                                moldura[0] = pagina
                                moldura[1] = tempo
                                moldura[2] = 1
                                moldura[3] = 0
                                substituida = True
                                break

                    # procura um caso classe 4: bit R=1 e bit M=1
                    if not substituida:
                        for moldura in matriz:
                            if moldura[2] == 1 and moldura[3] == 1:
                                moldura[0] = pagina
                                moldura[1] = tempo
                                moldura[2] = 1
                                moldura[3] = 0
                                substituida = True
                                break

            # tempo de ciclo
            if tempo % clock == 0:
                for moldura in matriz:
                    moldura[2] = 0  # reseta o bit R

    return print(pageMiss)

def relogio(vetor):
    pageMiss = 0 
    valores = []
    molduras = int(vetor[1]) #numero de molduras
    matriz = [[-1, 0, 0] for _ in range(molduras)] #matriz com 4 colunas por padrão e as linhas são o número de molduras
    clock = int(vetor[2]) #tempo em que o bit R vai zerar
    ponteiro = 0

    for i, linha in enumerate(vetor):
        if (i > 2): #n-3
            valores = linha.strip().split()
            pagina = int(valores[0]) #0 
            tempo = int(valores[1]) #0 -> tempo em que a página vai chegar

            # verifica se a página ja esta na memoria (matriz)
            pagina_na_memoria = False
            for j, moldura in enumerate(matriz):
                if (moldura[0] == pagina):
                    pagina_na_memoria = True
                    moldura[1] = tempo # seta o tempo da página acessada 
                    moldura[2] = 1 # bit R=1 -> modificado
                    break

            if not pagina_na_memoria:
                pageMiss +=1

                substituida = False
                while not substituida:
                    if matriz[ponteiro][2] == 0: # assim identifico em qual linha o ponteiro está
                        matriz[ponteiro][0] = pagina
                        matriz[ponteiro][1] = tempo
                        matriz[ponteiro][2] = 1 
                        substituida = True
                    else:
                        # reseta o bit R e avança o ponteiro
                        matriz[ponteiro][2] = 0
                        ponteiro = (ponteiro + 1) % molduras  # avança o ponteiro circularmente -> o ponteiro + proximo indice / numero de molduras. O resto será entre  e 0 e o último número, assim fazendo com que o ponteiro avance circularmente

                # avança o ponteiro usando o mesmo cálculo anterior
                ponteiro = (ponteiro + 1) % molduras

            # verifica o tempo de clock
            if tempo % clock == 0:
                for moldura in matriz:
                    moldura[2] = 0  # reseta o bit R

    return print(pageMiss)

class No:
    """Classe para representar um nó da lista encadeada circular."""
    def __init__(self, pagina):
        self.pagina = pagina
        self.referencia = 1  # Bit R = 1 quando a página entra na memória
        self.tempo = 0
        self.proximo = None  # Ponteiro para o próximo nó


class ListaCircularRelogio:
    """Lista encadeada circular para o algoritmo do Relógio."""
    def __init__(self, tamanho):
        self.tamanho = tamanho
        self.cabeca = None
        self.ponteiro = None  # Indica a posição do ponteiro do relógio
        self.elementos = 0  # Contador de elementos na lista

    def inserir(self, pagina, tempo):
        """Insere uma nova página na lista (substituindo se necessário)."""
        novo_no = No(pagina)
        novo_no.tempo = tempo

        if self.elementos < self.tamanho:
            # Ainda há espaço na memória, não precisa substituir
            if not self.cabeca:
                # Primeira inserção
                self.cabeca = novo_no
                self.ponteiro = novo_no
                novo_no.proximo = novo_no  # Aponta para ele mesmo (circular)
            else:
                # Insere no final da lista circular
                temp = self.cabeca
                while temp.proximo != self.cabeca:
                    temp = temp.proximo
                temp.proximo = novo_no
                novo_no.proximo = self.cabeca  # Fecha a lista circular

            self.elementos += 1
        else:
            # Memória cheia -> Aplicar substituição pelo Relógio
            self.substituir(novo_no)

    def substituir(self, novo_no):
        """Substitui uma página na memória usando a política do Relógio."""
        while True:
            if self.ponteiro.referencia == 0:
                # Encontramos uma página para substituição
                self.ponteiro.pagina = novo_no.pagina
                self.ponteiro.tempo = novo_no.tempo
                self.ponteiro.referencia = 1  # Página recém-inserida tem referência 1
                self.ponteiro = self.ponteiro.proximo  # Avança o ponteiro
                break
            else:
                # Se o bit R for 1, zere-o e avance o ponteiro
                self.ponteiro.referencia = 0
                self.ponteiro = self.ponteiro.proximo

    def atualizar_referencia(self, pagina):
        """Atualiza o bit de referência de uma página se ela for acessada."""
        temp = self.cabeca
        if not temp:
            return False
        
        for _ in range(self.tamanho):  # Percorre todas as molduras
            if temp.pagina == pagina:
                temp.referencia = 1  # Página foi acessada, então referência = 1
                return True
            temp = temp.proximo
        return False

    def reset_referencia(self):
        """Reseta todos os bits de referência na lista circular."""
        temp = self.cabeca
        if not temp:
            return
        
        for _ in range(self.tamanho):
            temp.referencia = 0
            temp = temp.proximo


def relogioSEC(vetor):
    """Função principal do algoritmo do Relógio."""
    pageMiss = 0
    molduras = int(vetor[1])  # Número de molduras na memória
    clock = int(vetor[2])  # Tempo de reset do bit R
    memoria = ListaCircularRelogio(molduras)  # Estrutura do relógio

    for i, linha in enumerate(vetor):
        if i > 2:  # Ignorar os três primeiros valores de entrada
            valores = linha.strip().split()
            pagina = int(valores[0])
            tempo = int(valores[1])

            # Verifica se a página já está na memória
            if not memoria.atualizar_referencia(pagina):
                pageMiss += 1
                memoria.inserir(pagina, tempo)

            # Reseta os bits R no tempo de clock
            if tempo % clock == 0:
                memoria.reset_referencia()

    print(pageMiss)


# função pra ler os txt
def lerArquivos(nomeArquivo):
        with open(nomeArquivo, "r") as arquivo:
            linhas = [linha.strip() for linha in arquivo]  # lendo as linhas
            print('leu')
        return linhas


# função pra escrever os arquivos
def escreverArquivos(vetor, nomeArquivo):
        with open(nomeArquivo, "w") as arquivo:
            for linha in vetor:
                arquivo.write(linha + '\n')  # escreve cada linha
        print('escreveu')


# testando os arquivos
arquivo_entrada = "TESTE-02.txt"
arquivo_saida = "RESULTADO-03.txt"

# lendo os arquivos (principalmente para o OTIMO que tem de prever o que deve ser removido)
linhas = lerArquivos(arquivo_entrada)
#pageMiss = nru(linhas)
#pageMiss = otimo(linhas)
pageMiss = relogioSEC(linhas)

     
