# Organização e Recuperação da Informação - Modelo Vetorial

Sistema de Busca que utiliza o Modelo Vetorial para processamento de consultas e cálculo de similaridade entre documentos, com ponderação de termos TF-IDF e índice invertido criado à partir da biblioteca SpaCy.

## Instalação e Execuação

### Pré-Requisitos

Os seguintes comandos devem ser executados de modo a fazer download dos pacotes necessários do SpaCy:

```bash
pip install -U spacy
pip install -U spacy-lookups-data
python3 -m spacy download pt_core_news_lg
```

### Execução

Dois arquivos devem ser passados para o programa via linha de comando. O primeiro arquivo deve conter os nomes (incluindo caminho, se necessário) de todos os documentos da base, um por linha. O segundo arquivo deve conter uma única linha, indicando a consulta que deve ser realizada. Ambos devem ser passados via linha de comando, substituindo-se ARQUIVO_BASE e CONSULTA baixo pelo arquivo com a base de documentos e o arquivo com a consulta, respectivamente.

```bash
python3 indice.py ARQUIVO_BASE CONSULTA

```

## Consulta

A consulta deve estar contida dentro de um arquivo em uma única linha. Os termos que compõem a consulta devem fazer parte da base e escritos segundo a seguinte sintaxe:

```plaintext
    TERMO1 & TERMO2 & TERMO3 ... & TERMON
```

## Corretor

Acesse o .pdf para detalhes sobre o uso do corretor.
