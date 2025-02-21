def otimo(vetor):
    pageMiss = 0
    molduras = []  
    numMolduras = int(vetor[1])  # numero total de molduras disponiveis
    numerosFuturos = []  # pega as páginas futuras

    # preenche a lista de numeros futuros
    for i, linha in enumerate(vetor):
        if i > 2:  # n-3
            valores = linha.strip().split()  
            if len(valores) >= 3: 
                numerosFuturos.append(valores[0])

    # iterando sobre páginas futuras
    for i, pagina in enumerate(numerosFuturos):
        if pagina not in molduras:  # se a página não está na moldura atual
            pageMiss += 1  # adiciona um pageMiss
            if len(molduras) < numMolduras:  # se ainda tiver o espaço (n=1)
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
                    if proximo_uso > indice_futuro:
                        indice_futuro = proximo_uso #indice é atualizado para o proximo uso
                        pagina_substituir = j # a pagina substituida atribui o valor do numero futuro atual

                # substitui a página mais distante
                molduras[pagina_substituir] = pagina
    print(pageMiss)
    return pageMiss


# Função para ler os arquivos .txt
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
arquivo_entrada = "TESTE-01.txt"
arquivo_saida = "RESULTADO-03.txt"

# lendo os arquivos (principalmente para o OTIMO que tem de prever o que deve ser removido)
linhas = lerArquivos(arquivo_entrada)

pageMiss = otimo(linhas)

     
