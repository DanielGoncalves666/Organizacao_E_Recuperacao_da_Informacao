# Organização e Recuperação da Informação - Índice Invertido

Criação de um Índice invertido à partir de uma base de arquivos, usando-se a biblioteca SpaCy para
processamento de linguagem natural.

## Instalação e Execuação

### Pré-Requisitos

Os seguintes comandos devem ser executados de modo a fazer download dos pacotes necessários do SpaCy:

```bash
pip install -U spacy
pip install -U spacy-lookups-data
python3 -m spacy download pt_core_news_lg
```

### Execução

Um arquivo deve conter os nomes (incluindo caminho, se necessário) de todos os documentos da base, um por linha.
Esse arquivo deve ser passado para o programa via linha de comando, substituindo ARQUIVO_BASE abaixo:

```bash
python3 indice.py ARQUIVO_BASE

```

## Corretor

Acesse o .pdf para detalhes sobre o uso do corretor.
