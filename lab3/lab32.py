import os
import time
import heapq
from dimacs import *


class Node:
    def __init__(self) -> None:
        self.edges = {}

    def addEdge(self, to, weight):
        self.edges[to] = self.edges.get(to, 0) + weight

    def delEdge(self, to):
        del self.edges[to]


def convert_graph(V, L):
    graph = [Node() for _ in range(V)]
    for u, v, w, in L:
        graph[u-1].addEdge(v-1, w)
        graph[v-1].addEdge(u-1, w)

    return graph


def StoerWagner(graph):  # graph = list of nodes (type Node[])

    def mergeVertices(graph, x, y):
        nonlocal V

        for u in graph[y].edges:
            w = graph[y].edges[u]
            if u != x:
                graph[u].addEdge(x, w)
                graph[x].addEdge(u, w)
            graph[u].delEdge(y)

        graph[y] = Node()
        V -= 1

    def minimumCutPhase(graph):
        s, t = 0, 0
        processed = [False for _ in range(len(graph))]
        weightSum = [0 for _ in range(len(graph))]

        heap = []
        heapq.heappush(heap, (0, 0))
        while len(heap) > 0:
            u = heapq.heappop(heap)[1]
            if not processed[u]:
                processed[u] = True
                s, t = u, s
                for v in graph[u].edges:
                    if not processed[v]:
                        weightSum[v] += graph[u].edges[v]
                        heapq.heappush(heap, (-weightSum[v], v))

        tmp_ans = 0
        for u in graph[s].edges:
            tmp_ans += graph[s].edges[u]

        mergeVertices(graph, s, t)
        return tmp_ans

    V = len(graph)
    ans = float('inf')
    while V > 1:
        ans = min(ans, minimumCutPhase(graph))

    return ans


def test():  # Testy

    directory = 'graphs-lab3'
    max_time = 200

    NumCorrect = 0
    NumOfTests = 0

    for filename in os.listdir(directory):

        f = os.path.join(directory, filename)

        with open(f) as F:
            first_line = F.readline()
            words = first_line.split()
        V, L = loadWeightedGraph(f)

        start = time.time()
        ans = StoerWagner(convert_graph(V, L))
        end = time.time()
        T = end - start
        print(f)
        print("Oczekiwany wynik:", int(words[-1]))

        if ans == int(words[-1]) and T <= max_time:
            print("Wynik:", ans, "|", "%.2f" % T, "s", "|", "OK!")
            NumCorrect += 1

        elif T > max_time:
            print("Wynik:", ans, "|", "%.2f" % T, "s", "|", "Za wolno!")

        else:
            print("Wynik:", ans, "|", "%.2f" % T, "s", "|", "Błąd!")

        NumOfTests += 1

        print("-----------------")

    print(NumCorrect, "/", NumOfTests)


test()
