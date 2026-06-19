import igraph as ig
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import random
import time
import scipy.stats as st

node_map = {}
edges = []

with open("p2p-Gnutella05.txt", "r") as f:
    for line in f:
        if line.startswith("#"): 
            continue
        u_str, v_str = line.strip().split()
        u, v = int(u_str), int(v_str)
        
        if u not in node_map: node_map[u] = len(node_map)
        if v not in node_map: node_map[v] = len(node_map)
        edges.append((node_map[u], node_map[v]))

g = ig.Graph(n=len(node_map), edges=edges, directed=False)
g.simplify(multiple=True, loops=True)
v_count = g.vcount()

degrees = g.degree()
min_deg = min(degrees)
max_deg = max(degrees)
avg_deg = sum(degrees) / v_count
density = g.density()

components = g.connected_components()
lcc_size = len(components.giant().vs)

clustering_coeff = g.transitivity_undirected()
triangles = len(g.cliques(min=3, max=3))

sample_nodes = random.sample(range(v_count), min(500, v_count))
shortest_paths = g.distances(source=sample_nodes)
valid_paths = [p for sp_list in shortest_paths for p in sp_list if p > 0 and p != float('inf')]
diametro = max(valid_paths) if valid_paths else 0
caminho_medio = sum(valid_paths) / len(valid_paths) if valid_paths else 0

print(f"V: {v_count} | E: {g.ecount()}")
print(f"Grau -> Min: {min_deg} | Max: {max_deg} | Medio: {avg_deg:.2f}")
print(f"Densidade: {density:.8f}")
print(f"Componentes conexas: {len(components)} | LCC: {lcc_size}")
print(f"Clusterizacao: {clustering_coeff:.6f} | Triangulos: {triangles}")
print(f"Diametro: {diametro} | Caminho medio: {caminho_medio:.2f}\n")

n_runs = 30
resultados_tempo = {"BFS": [], "DFS": [], "Dijkstra": [], "Kruskal": [], "Tarjan": []}

for _ in range(n_runs):
    start = time.perf_counter()
    g.bfs(0)
    resultados_tempo["BFS"].append(time.perf_counter() - start)
    
    start = time.perf_counter()
    g.dfs(0)
    resultados_tempo["DFS"].append(time.perf_counter() - start)
    
    start = time.perf_counter()
    g.distances(source=0, weights=[1]*g.ecount())
    resultados_tempo["Dijkstra"].append(time.perf_counter() - start)
    
    start = time.perf_counter()
    g.spanning_tree()
    resultados_tempo["Kruskal"].append(time.perf_counter() - start)
    
    start = time.perf_counter()
    g.connected_components()
    resultados_tempo["Tarjan"].append(time.perf_counter() - start)

print(f"{'Algoritmo':<12} | {'Media (s)':<12} | {'Desvio Padrao':<15} | {'IC (95%)'}")
for alg, tempos in resultados_tempo.items():
    media = np.mean(tempos)
    dp = np.std(tempos, ddof=1)
    ic = st.norm.interval(0.95, loc=media, scale=dp/np.sqrt(n_runs))
    print(f"{alg:<12} | {media:.6f}     | {dp:.6f}        | [{ic[0]:.6f}, {ic[1]:.6f}]")

T = 30
n_remover = int(0.05 * v_count)

metricas_A, metricas_B, metricas_C, metricas_D = [], [], [], []

for _ in range(T):
    g_temp = g.copy()
    alvos = random.sample(range(v_count), n_remover)
    g_temp.delete_vertices(alvos)
    
    comps = g_temp.connected_components()
    lcc = comps.giant()
    
    metricas_A.append(len(lcc.vs))
    metricas_B.append(len(comps))
    
    sample = random.sample(range(g_temp.vcount()), min(100, g_temp.vcount()))
    paths = g_temp.distances(source=sample)
    valid_paths_T = [p for sublist in paths for p in sublist if p > 0 and p != float('inf')]
    avg_path = sum(valid_paths_T) / len(valid_paths_T) if valid_paths_T else 0
    metricas_C.append(avg_path)
    
    isolados = sum(1 for d in g_temp.degree() if d == 0)
    metricas_D.append(isolados / g_temp.vcount())

nos_ordenados = sorted(range(v_count), key=lambda x: degrees[x], reverse=True)
alvos_ataque = nos_ordenados[:n_remover]

g_ataque = g.copy()
g_ataque.delete_vertices(alvos_ataque)

comps_ataque = g_ataque.connected_components()
lcc_ataque = comps_ataque.giant()
metrica_A_ataque = len(lcc_ataque.vs)
metrica_B_ataque = len(comps_ataque)

sample_atk = random.sample(range(g_ataque.vcount()), min(100, g_ataque.vcount()))
paths_atk = g_ataque.distances(source=sample_atk)
valid_paths_atk = [p for sublist in paths_atk for p in sublist if p > 0 and p != float('inf')]
metrica_C_ataque = sum(valid_paths_atk) / len(valid_paths_atk) if valid_paths_atk else 0

isolados_ataque = sum(1 for d in g_ataque.degree() if d == 0)
metrica_D_ataque = isolados_ataque / g_ataque.vcount()

print(f"\nAtaque Direcionado -> A: {metrica_A_ataque} | B: {metrica_B_ataque} | C: {metrica_C_ataque:.2f} | D: {metrica_D_ataque:.4f}\n")

counts = np.bincount(degrees)
k = np.nonzero(counts)[0]
p_k = counts[k] / sum(counts)

plt.figure(figsize=(8, 6))
plt.loglog(k, p_k, marker='o', linestyle='none', markersize=5, color='darkred')
plt.title("Distribuicao de Graus - p2p-Gnutella05")
plt.xlabel("Grau (k)")
plt.ylabel("Probabilidade P(k)")
plt.grid(True, which="both", ls="--", alpha=0.5)
plt.savefig("distribuicao_graus.png", dpi=300)
plt.close()

max_degree_node = np.argmax(degrees)
neighbors = g.neighbors(max_degree_node)
subgraph_nodes = [max_degree_node] + neighbors
sub_g = g.subgraph(subgraph_nodes)

nx_g = nx.Graph(sub_g.get_edgelist())
plt.figure(figsize=(7, 7))

subgraph_nodes_sorted = sorted(subgraph_nodes)
hub_new_id = subgraph_nodes_sorted.index(max_degree_node)

color_map = ['red' if node == hub_new_id else 'skyblue' for node in nx_g.nodes()]
size_map = [400 if node == hub_new_id else 50 for node in nx_g.nodes()]
pos = nx.spring_layout(nx_g, seed=42)

nx.draw(nx_g, pos, node_color=color_map, node_size=size_map, edge_color='gray', alpha=0.7)
plt.title(f"Subgrafo: Hub Central (Grau {degrees[max_degree_node]})")
plt.savefig("subgrafo_gnutella.png", dpi=300)
plt.close()

fig, axs = plt.subplots(2, 2, figsize=(12, 10))
fig.suptitle('Robustez - Falhas Aleatorias', fontsize=16)

axs[0, 0].boxplot(metricas_A, patch_artist=True)
axs[0, 0].set_title('Metrica A')

axs[0, 1].boxplot(metricas_B, patch_artist=True)
axs[0, 1].set_title('Metrica B')

axs[1, 0].boxplot(metricas_C, patch_artist=True)
axs[1, 0].set_title('Metrica C')

axs[1, 1].boxplot(metricas_D, patch_artist=True)
axs[1, 1].set_title('Metrica D')

plt.tight_layout()
plt.savefig("boxplots_robustez.png", dpi=300)
plt.close()