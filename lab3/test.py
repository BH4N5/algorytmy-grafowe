import heapq
import random
from dimacs import *


def stoer_wagner(V, L):
    graph = [[] for _ in range(V)]
    edges = [0 for i in range(V)]
    visited = [False for i in range(V)]
    s = [0 for i in range(V)]

    for (u, v, e) in L:
        graph[u-1].append(v-1)
        graph[v-1].append(u-1)

    a = 0
    for u in range(len(graph)):
        if len(graph[u]) < len(graph[a]):
            a = u

    que = [[0, a]]
    for i in range(V):
        while True:
            u = heapq.heappop(que)[1]
            if not visited[u]:
                break
        s[i] = u
        visited[u] = True
        if i == V - 1:
            final_connectivity = edges[u]

        for v in graph[u]:
            if visited[v]:
                continue
            edges[v] += 1
            heapq.heappush(que, (-edges[v], v))
    print(s)
    curr_connectivity = 0
    merged_weights = [0 for i in range(V)]
    merged_visited = [False for i in range(V)]
    for u in s[:-1]:
        merged_visited[u] = True
        curr_connectivity -= merged_weights[u]
        for v in graph[u]:
            if not merged_visited[v]:
                merged_weights[v] += 1
                curr_connectivity += 1
        final_connectivity = min(curr_connectivity, final_connectivity)

    return final_connectivity


def StoerWagner(graph):
    # graph = adjacency matrix; time complexity O(V^3); assuming nontrivial
    # input i.e. connectivity(graph) > 0

    def mergeVertices(graph, s, t):  # O(V)
        for u in range(len(graph)):
            if u != s:
                graph[s][u] += graph[t][u]
                graph[u][s] += graph[t][u]
            graph[t][u] = 0
            graph[u][t] = 0

    def minimumCutPhase(graph):
        S = []
        s, t = 0, 0
        processed = [False for _ in range(len(graph))]
        weightSum = [0 for _ in range(len(graph))]

        for _ in range(len(graph)):
            u = weightSum.index(max(weightSum))
            if not processed[u]:
                S.append(u)
                s, t = u, s
                weightSum[u] = 0
                processed[u] = True
                for v in range(len(graph)):
                    if not processed[v]:
                        weightSum[v] += graph[u][v]

        tmp_ans = sum(graph[s])
        mergeVertices(graph, s, t)
        print(S)
        return tmp_ans

    ans = float('inf')
    for _ in range(len(graph)-1):
        ans = min(ans, minimumCutPhase(graph))

    return ans


def convert_graph(V, L):
    graph = [[0 for _ in range(V)] for _ in range(V)]
    for u, v, w in L:
        graph[u-1][v-1] = w
        graph[v-1][u-1] = w

    return graph


def genRndGraph(n):
    graph = [[0 for _ in range(n)] for _ in range(n)]
    for u in range(len(graph)):
        e = random.randint(n//2, n)
        for _ in range(e):
            v = random.randint(0, n-1)
            if u != v:
                graph[u][v] = 1
        if u < n-1:
            graph[u][u+1] = 1
            graph[u+1][u] = 1
        else:
            graph[u][0] = 1
            graph[0][u] = 1
    L = []
    for u in range(len(graph)):
        for v in range(u+1, len(graph)):
            if graph[u][v] == 1:
                L.append((u+1, v+1, 1))

    return L


def genTests(N):
    numCorrect = 0
    numIncorrect = 0
    for _ in range(N):
        V = random.randint(10, 12)
        L = genRndGraph(V)
        a, b = StoerWagner(convert_graph(V, L)), stoer_wagner(V, L)
        if a != b:
            print(V)
            print(L)
            print("Moj:", a, "|", "Inny", b)
            numIncorrect += 1
        else:
            numCorrect += 1

    print("Correct", numCorrect, "|", "Incorrect", numIncorrect)


# genTests(1000)

V = 6
L = [(1, 2, 1), (1, 3, 1), (1, 4, 1), (2, 3, 1), (3, 4, 1),
     (2, 5, 1), (3, 5, 1), (4, 5, 1), (1, 5, 1), (1, 6, 1), (5, 6, 1)]

print(StoerWagner(convert_graph(V, L)))
print(stoer_wagner(V, L))
