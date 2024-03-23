#Daniel Gonçalves - 12011BCC011

import spacy
from math import (log, sqrt)
import sys 
# O pacote sys foi usado para se obter os argumento passados por linha de comando.
# Uma alternativa seria o pacote argparse, mas como se espera apenas dois argumentos, o sys é suficiente.

def criarMatriz(numLinhas, numColunas):            
    matriz = []
    
    if numLinhas == 1:
        return [0] * numColunas
    
    for _ in range(numLinhas):
        linha = [0] * numColunas
        matriz.append(linha)
        
    return matriz

class indiceInvertido:
    __dic = {}
    termos = []
    numDocs = 0
    nomeDocs = []
    
    def adicionarIndiceDocumento(self, indiceDoc: dict, docIndex: int, nomeDoc):
        
        for termo in indiceDoc.keys():
            if termo not in self.__dic:
                self.__dic[termo] = [(docIndex, indiceDoc[termo])]
                self.termos.append(termo)
            else:
                anteriores = self.__dic[termo]
                anteriores.append((docIndex,indiceDoc[termo]))
                
        self.numDocs += 1
        self.nomeDocs.append(nomeDoc)  
        self.termos.sort()      
                
    def indiceToFile(self, name="indice.txt"):        
        with open(name,mode="w") as indice:
            for termo in self.termos:
                listaDocQtd = self.__dic[termo]
               
                stringToWrite = f"{termo}:"
                for (doc, qtd) in listaDocQtd:
                   stringToWrite += f" {doc},{qtd}"
                   
                stringToWrite += "\n"
                
                indice.write(stringToWrite)           
    
    def getDic(self):
        return self.__dic
            
class ponderador:
    idf = []
    #docs são linhas, termos são colunas (tf e tf_idf)
    tf = []
    tf_idf = [] 
    
    def __init__(self, index: indiceInvertido):
        self.__dic = index.getDic()
        self.termos = index.termos
        self.numDocs = index.numDocs
        self.nomeDocs = index.nomeDocs
            
    def __ponderarIDF(self): 
        self.idf = criarMatriz(1,len(self.termos))
               
        for i in range(len(self.termos)):
            ni = len(self.__dic[self.termos[i]])
            self.idf[i] = log((self.numDocs/ni),10)
            
    def __ponderarTF(self):
        numTermos = len(self.termos)   
        self.tf = criarMatriz(self.numDocs, numTermos)

        for i in range(numTermos):            
            frequencias = self.__dic[self.termos[i]]
            for (doc, freq) in frequencias:
                # docs são numerados de 1 até numDocs, incluso.
                self.tf[doc - 1][i] = 1 + log(freq, 10)
                
    def ponderarTF_IDF(self):
        self.__ponderarTF()
        self.__ponderarIDF()
        
        numTermos = len(self.termos)
        self.tf_idf = criarMatriz(self.numDocs, numTermos)
        
        for i in range(self.numDocs):
            for h in range(numTermos):
                self.tf_idf[i][h] = 0 if self.tf[i][h] == 0 else self.tf[i][h] * self.idf[h]
            
        return self.tf_idf
    
    def ponderacaoToFile(self, name="pesos.txt"):
        with open(name,mode="w") as pesos:
            for docNumber in range(self.numDocs):
                stringToWrite = f"{self.nomeDocs[docNumber]:}"
                
                for termNumber in range(len(self.termos)):
                    if self.tf_idf[docNumber][termNumber] == 0:
                        continue
                    
                    stringToWrite += f" {self.termos[termNumber]},{self.tf_idf[docNumber][termNumber]}"
                
                stringToWrite += "\n"
                
                pesos.write(stringToWrite)               
 
class consulta:
    __termos = []
    c_tf = []
    c_tf_idf = []
    similaridades = []
    
    def __init__(self, query):
        self.preProcessamento(query)

    def preProcessamento(self, query):
        nlp = spacy.load("pt_core_news_lg") #carrega o modelo da língua portuguesa
        
        query = query.upper() # necessário para impedir o caso onde jessica é lematizado como jessico
        termos = query.split(" ")
        
        preQuery = []
        for i in termos:
            if i == "&":
                continue
            
            preQuery.append(i) # contém apenas os termos agora
            
        self.__termos = analiseSpacy(nlp, " ".join(preQuery))
            
    def ponderarConsulta(self, pond: ponderador):
        numTermos = len(pond.termos)
        
        self.c_tf = criarMatriz(1,numTermos)
        self.c_tf_idf = criarMatriz(1,numTermos)

        indiceConsulta = determinarFrequenciaTermos(self.__termos)
        
        for termo in self.__termos:
            try:
                h = pond.termos.index(termo) #posição do termo no vetor que indica um documento
                self.c_tf[h] = 1 + log(indiceConsulta[termo], 10)
                self.c_tf_idf[h] = self.c_tf[h] * pond.idf[h]
            except ValueError:
                print(f"{termo} não presente na base.")
                exit(0)
          
    def determinarRespostaConsulta(self, pond: ponderador):            
        for docNum in range(pond.numDocs):
            s = self.__similaridadeQueryDoc(pond.tf_idf[docNum])
            
            if s < 0.001:
                continue # doc não atende ao patamar mínimo
            
            self.similaridades.append((pond.nomeDocs[docNum], s))
            
        self.similaridades.sort(key = lambda doc: doc[1], reverse=True)
            
    
    def __similaridadeQueryDoc(self, doc):
        produtoInterno = 0
        normaEuclidianaQuery = 0
        normaEuclidianaDoc = 0
        for i in range(len(doc)):
            produtoInterno += self.c_tf_idf[i] * doc[i]
            normaEuclidianaQuery += self.c_tf_idf[i] ** 2
            normaEuclidianaDoc += doc[i] ** 2
            
        return produtoInterno / (sqrt(normaEuclidianaQuery) * sqrt(normaEuclidianaDoc))
    
    def respostaConsultaToFile(self, name="resposta.txt"):
        with open(name,mode="w") as resposta:
            resposta.write(f"{len(self.similaridades)}\n")
            for (docName,sim) in self.similaridades:
                stringToWrite = f"{docName} {sim}\n"
                resposta.write(stringToWrite) 
            
def abrirDocsBase(nomeArquivoBase):    
    documentos = []
    
    try:
        with open(nomeArquivoBase) as arquivoBase:
            for nomeDoc in arquivoBase:
                if nomeDoc == "\n":
                    continue
                
                if nomeDoc[-1] == '\n':
                    nomeDoc = nomeDoc[0:-1]

                try:
                    documentos.append((open(nomeDoc),nomeDoc))
                except FileNotFoundError:
                    print(f"Documento {nomeDoc} não foi encontrado.")
                    continue #ignora documentos não encontrados
    except FileNotFoundError:
        print("Documento da base não encontrado.")
        exit(0)
            
    return documentos

def tratarDocumentos(index: indiceInvertido, documentos):
    nlp = spacy.load("pt_core_news_lg") #carrega o modelo da língua portuguesa
    
    for i in range(len(documentos)):   
        (docPointer, docName) = documentos[i]
        docText = docPointer.read()
        
        docProcessado = analiseSpacy(nlp, docText)
        indiceDocAtual = determinarFrequenciaTermos(docProcessado)
        index.adicionarIndiceDocumento(indiceDocAtual, i + 1, docName)
        
    for (doc,_) in documentos:
        doc.close()   
        
def determinarFrequenciaTermos(doc):
    indiceDoc = {}
        
    for termo in doc:
        if termo not in indiceDoc:
            indiceDoc[termo] = 1
        else:
            valorAtual = indiceDoc[termo]
            indiceDoc[termo] = valorAtual + 1
    
    return indiceDoc
    
def analiseSpacy(nlp, text):
    doc = nlp(text)
    
    docSemPunct = [t for t in doc if not t.is_punct and not t.is_space]
    docSemEspacos = [t for t in docSemPunct if t.orth not in ['\n']]
    
    docSemStopWords = [t for t in docSemEspacos if not t.is_stop]
    docLematizado = [t.lemma_ for t in docSemStopWords]
    docSemLemmasCompostos = [t.lower() for t in docLematizado if ' ' not in t]  # para dar igual ao corretor
    # esse lower é necessário pois nlp(), na hora de criar os tokens, cria aqueles com nome próprio
    # com inicial maiúscula; além disso, é necessário para considerar maiúsculas e minúsculas iguais    
    
    return docSemLemmasCompostos

def obterConsulta(nomeArquivoConsulta):
    try:
        with open(nomeArquivoConsulta) as arq:
            query = arq.readline()
            
            if query == "" or query == "\n":
                print("Consulta inválida.")
                arq.close()
                exit(0)
                
            if query[-1] == '\n':
                query = query[0:-1]
                
            return query
    except FileNotFoundError:
        print("Arquivo da consulta não encontrado.")
        exit(0)
            
if __name__ == "__main__":
    nomeArquivoBase = sys.argv[1]
    nomeArquivoConsulta = sys.argv[2]
    
    documentos = abrirDocsBase(nomeArquivoBase)
    index = indiceInvertido()
    tratarDocumentos(index, documentos)
    index.indiceToFile()
    
    pond = ponderador(index)
    pond.ponderarTF_IDF()
    pond.ponderacaoToFile()
    
    query = obterConsulta(nomeArquivoConsulta)
    consul = consulta(query)
    consul.ponderarConsulta(pond)
    consul.determinarRespostaConsulta(pond)
    consul.respostaConsultaToFile()
