import sys
import matplotlib.pyplot as plt

vetSaidasIdeias = []
vetSaidasSistema = []

def processar_arquivo(nomeArquivo):
    
    try:
        with open(nomeArquivo, "r") as arq:
            numConsultas = int(arq.readline().strip("\n"))

            for _ in range(numConsultas):
                vetSaidasIdeias.append(list(map(int, arq.readline().strip("\n").split(" "))))
                
            for _ in range(numConsultas):
                vetSaidasSistema.append(list(map(int, arq.readline().strip("\n").split(" "))))
                
        return numConsultas
            
    except FileNotFoundError:
        print("Arquivo de referência não encontrado.")
        exit()
    except ValueError:
        print("Sintaxe do arquivo errada. Verifique por linhas vazias e/ou caracteres não numéricos.")
        exit()
        
def determinar_metricas(numConsultas):
    vetNiveisPadrao = [1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0]
    resposta = []
    
    for c in range(numConsultas):
        numDocsRelevantes = len(vetSaidasIdeias[c])
        vetPrecRevoc = []
        
        docsRelevantes = 0
        totalDocs = 0
        for doc in vetSaidasSistema[c]:
            totalDocs += 1
            
            if doc in vetSaidasIdeias[c]:
                docsRelevantes += 1
                
                # (precisão, revocação)
                vetPrecRevoc.append((docsRelevantes / totalDocs, docsRelevantes / numDocsRelevantes))
                # Mudanças de precisões entre mudanças de revocação podem ser ignoradas pois serão menores
                # que a precisão da última mudança de revocação e vem antes da próximo mudança (logo não 
                # serão usadas por nenhum nível padrão de revocação).
                                
        maiorPrecisao = 0
        vetPrecPadrao = [] # vetor com correspondências de precisão com os 11 níveis padrão de revocação
        nivelAtual = 0
           
        for (prec, revoc) in vetPrecRevoc[::-1]:    
            # recoc + 1e-10 está acima da precisão (float) requerida pra ser considerada igual
            while vetNiveisPadrao[nivelAtual] >= revoc + 1e-10:
                vetPrecPadrao.insert(0,maiorPrecisao)
                nivelAtual += 1
            # o while acima serve pra preencher com o maior valor de precisao todos os niveis de revocação
            # maiores que revoc
                
            maiorPrecisao = max(prec, maiorPrecisao)
            
            # caso o revoc for igual a um dos níveis padrão
            if abs(revoc - vetNiveisPadrao[nivelAtual]) < 1e-10: 
                vetPrecPadrao.insert(0,maiorPrecisao)
                nivelAtual += 1
                
        # preenche as precisões para os níveis de revocação menores que o menor valor de revoc
        while nivelAtual < len(vetNiveisPadrao):
            vetPrecPadrao.insert(0,maiorPrecisao)
            nivelAtual += 1
                 
        resposta.append(vetPrecPadrao)
        
        #vetNiveisPadrao foi criado ao contrário
    return (vetNiveisPadrao[::-1], resposta)

def calcularMedia(respostas):
    medias = [0] * 11
    
    for atual in respostas:
        for i in range(len(medias)):
            medias[i] += atual[i] / len(respostas)

    return medias

def mediasToFile(medias):
    with open("media.txt", "w") as saida:
        string = str(medias[0])       
        for valor in medias[1:]:
            string += f" {valor}"
            
        saida.write(string)

def plotarGrafico(eixoX, eixoY, titulo, figura):
    plt.figure(figura)
    plt.plot(eixoX, eixoY)
    plt.title(titulo)
    plt.xlabel("Nível padrão de revocação")
    plt.ylabel("Precisão")    

if __name__ == "__main__":
    nomeArquivoIdeal = sys.argv[1]
    
    numConsultas = processar_arquivo(nomeArquivoIdeal)
    vetNiveis, respostas = determinar_metricas(numConsultas)
    medias = calcularMedia(respostas)

    mediasToFile(medias)
    
    vetNiveis = list(map(lambda x: x * 100, vetNiveis))
    
    ultimo = 0
    for i in range(len(respostas)):
        plotarGrafico(vetNiveis, list(map(lambda x: x * 100, respostas[i])), f"Consulta {i + 1}", i)
        ultimo = i
        
    plotarGrafico(vetNiveis, list(map(lambda x: x * 100, medias)), "Médias", ultimo + 1)
    plt.show()
