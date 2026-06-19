# P2P Gnutella Graph Analysis

Este repositório contém um script em Python (`script.py`) para analisar a rede P2P Gnutella (dataset `p2p-Gnutella05.txt`) utilizando conceitos de Teoria dos Grafos.

## O que o script faz?

O script realiza diversas análises estruturais e de desempenho sobre o grafo da rede:

1. **Leitura e Construção do Grafo:** Lê o arquivo `p2p-Gnutella05.txt` e constrói um grafo não-direcionado utilizando a biblioteca `igraph`.
2. **Métricas Básicas:** Calcula o número de vértices (V) e arestas (E), graus mínimo, máximo e médio, além da densidade da rede.
3. **Métricas Estruturais:** Determina as componentes conexas, o tamanho da maior componente conexa (LCC), coeficiente de clusterização, contagem de triângulos, diâmetro e caminho médio.
4. **Desempenho de Algoritmos:** Executa os algoritmos BFS, DFS, Dijkstra, Kruskal e Tarjan 30 vezes cada, calculando a média de tempo, desvio padrão e intervalo de confiança (95%).
5. **Análise de Robustez (Falhas e Ataques):**
   - **Falhas Aleatórias:** Remove aleatoriamente 5% dos nós (repetido 30 vezes) e avalia o impacto na rede (tamanho do LCC, número de componentes, caminho médio e proporção de nós isolados).
   - **Ataque Direcionado:** Remove os 5% dos nós com os maiores graus (hubs) e avalia o impacto nas mesmas métricas.
6. **Geração de Gráficos:** Cria e salva as seguintes imagens:
   - `distribuicao_graus.png`: Gráfico log-log da distribuição de graus da rede.
   - `subgrafo_gnutella.png`: Visualização do subgrafo contendo o nó de maior grau (Hub Central) e seus vizinhos.
   - `boxplots_robustez.png`: Boxplots ilustrando o impacto das falhas aleatórias nas métricas da rede.

## Como rodar o script

### Pré-requisitos

Certifique-se de ter o Python instalado em sua máquina. Além disso, você precisará instalar as bibliotecas utilizadas no script.

Você pode instalar todas as dependências rodando o seguinte comando no terminal:

```bash
pip install igraph matplotlib numpy networkx scipy
```

### Execução

1. Certifique-se de que o arquivo de dados `p2p-Gnutella05.txt` está no mesmo diretório que o script.
2. Abra o terminal na pasta do projeto e execute:

```bash
python script.py
```

3. Os resultados textuais serão exibidos diretamente no console.
4. As imagens geradas (`distribuicao_graus.png`, `subgrafo_gnutella.png` e `boxplots_robustez.png`) serão salvas na mesma pasta do script.
