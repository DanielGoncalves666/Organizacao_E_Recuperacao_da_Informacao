# Organização e Recuperação da Informação - Precisão e Revocação

Cálculo das métricas e plotagem de gráficos de Precisão e Revocação (Cobertura) para um conjunto de dados simulando um sistema de busca em teste.

## Instalação e Execuação

### Pré-Requisitos

Os seguintes comandos devem ser executados de modo a fazer download dos pacotes necessários do matplotlib:

```bash
python3 -m pip install -U matplotlib
```

### Execução

Um arquivo deve ser passado para o programa via linha de comando. Esse arquivo contém três partes:

1 - Compreendo a primeira linha, contém um único inteiro (N) indicando o número de consultas.

2 - As próximas N linhas contém, em cada uma, a saídas ideal para cada uma das N consultas.

3 - As N linhas seguintes contém, em cada uma, a resposta obtida pelo sistema em avaliação.

```bash
python3 avaliacao.py ARQUIVO

```

## Corretor

Acesse o .pdf para detalhes sobre o uso do corretor.
