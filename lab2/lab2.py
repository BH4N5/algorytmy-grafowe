import os
import time
from dimacs import *
import collections


def convert_graph(V, L):
    G = [[0 for i in range(V)] for j in range(V)]
    LS = [[] for v in range(V)]
    for u, v, w in L:
        G[u-1][v-1] = w
        LS[u-1].append(v-1)
        LS[v-1].append(u-1)

    return G, LS


def bfs(graph, ls, s, t, parent):
    visited = [False] * len(graph)
    queue = collections.deque()
    queue.append(s)
    visited[s] = True
    while queue:
        u = queue.popleft()
        for v in ls[u]:
            if not visited[v] and graph[u][v] > 0:
                queue.append(v)
                visited[v] = True
                parent[v] = u
    return visited[t]


def EdmondsKarp(P, s, t):
    graph, ls = P
    parent = [-1] * len(graph)
    max_flow = 0
    while bfs(graph, ls, s, t, parent):
        flow = float("Inf")
        u = t
        while u != s:
            flow = min(flow, graph[parent[u]][u])
            u = parent[u]
        max_flow += flow
        v = t
        while v != s:
            u = parent[v]
            graph[u][v] -= flow
            graph[v][u] += flow
            v = parent[v]
    return max_flow

# Program testujący


def test():

    total_time = 0
    Num_correct = 0
    Num = 0
    directory = 'flow'
    max_time = 100
    for filename in os.listdir(directory):

        f = os.path.join(directory, filename)

        with open(f) as F:
            first_line = F.readline()
            words = first_line.split()
        V, L = loadDirectedWeightedGraph(f)

        start = time.time()
        ans = EdmondsKarp(convert_graph(V, L), 0, V-1)
        end = time.time()
        T = end - start
        print(f)
        print("Oczekiwany wynik:", int(words[-1]))

        if ans == int(words[-1]) and T <= max_time:
            print("Wynik:", ans, "|", "%.2f" % T, "s", "|", "OK!")
            Num_correct += 1

        elif T > max_time:
            print("Wynik:", ans, "|", "%.2f" % T, "s", "|", "Za wolno!")

        else:
            print("Wynik:", ans, "|", "%.2f" % T, "s", "|", "Błąd!")

        Num += 1

        print("-----------------")

    print(Num_correct, "/", Num)


test()
