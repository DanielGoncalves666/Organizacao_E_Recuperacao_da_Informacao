#Daniel Gonçalves - 12011BCC011

import spacy
import sys 
# O pacote sys foi usado para se obter o argumento passado por linha de comando.
# Uma alternativa seria o pacote argparse, mas como se espera apenas um argumento, o sys é suficiente.

class indiceInvertido:
    __dic = {}

    def adicionarIndiceDocumento(self, indiceDoc: dict, doc: int):
        
        for termo in indiceDoc.keys():
            if termo not in self.__dic:
                self.__dic[termo] = [(doc, indiceDoc[termo])]
            else:
                anteriores = self.__dic[termo]
                anteriores.append((doc,indiceDoc[termo]))
                
    def indiceToFile(self):
        termos = [ i for i in self.__dic.keys()]
        termos.sort()
        
        with open("indice.txt",mode="w") as indice:
            for termo in termos:
                listaDocQtd = self.__dic[termo]
               
                stringToWrite = f"{termo}:"
                for (doc, qtd) in listaDocQtd:
                   stringToWrite += f" {doc},{qtd}"
                   
                stringToWrite += "\n"
                
                indice.write(stringToWrite)           
            
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
                    documentos.append(open(nomeDoc))
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
        docText = documentos[i].read()
        doc = nlp(docText)
        
        docSemPunct = [t for t in doc if not t.is_punct and not t.is_space]
        docSemEspacos = [t for t in docSemPunct if t.orth not in ['\n']]
        
        docSemStopWords = [t for t in docSemEspacos if not t.is_stop]
        docLematizado = [t.lemma_ for t in docSemStopWords]
        docSemLemmasCompostos = [t.lower() for t in docLematizado if ' ' not in t]  # para dar igual ao corretor
        # esse lower é necessário pois nlp(), na hora de criar os tokens, cria aqueles com nome próprio
        # com inicial maiúscula; além disso, é necessário para considerar maiúsculas e minúsculas iguais
        
        indiceDocAtual = {}
        
        for termo in docSemLemmasCompostos:
            if termo not in indiceDocAtual:
                indiceDocAtual[termo] = 1
            else:
                valorAtual = indiceDocAtual[termo]
                indiceDocAtual[termo] = valorAtual + 1
                
        index.adicionarIndiceDocumento(indiceDocAtual, i + 1)
    
def fecharDocsBase(documentos):
    for doc in documentos:
        doc.close()   

if __name__ == "__main__":
    nomeArquivoBase = sys.argv[1]
    
    documentos = abrirDocsBase(nomeArquivoBase)
    
    index = indiceInvertido()
    
    tratarDocumentos(index, documentos)
    
    index.indiceToFile()

    fecharDocsBase(documentos)    