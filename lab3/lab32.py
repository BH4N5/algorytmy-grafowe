import os
import time
from dimacs import *

'''
Poniżej zaimplementowano algorytm Stoera-Wagnera dla grafu reprezentowanego
przez macierz sąsiedztwa graph[u][v]. Funkcja mergeVertices() odpowiada za
scalanie wierzchołków i jest łatwa do zaimplementowania w złożoności O(V) dla
reprezentacji grafu w postaci macierzy sąsiedztwa.

Ze względu na wykorzystanie reprezenatcji macierzowej złożoność czasowa
algorytmu to O(V^3). Dla grafów rzadkich jest ona gorsza od docelowej złożoności
O(V*E + V^2 log V) uzyskiwanej poprzez wykorzystanie kolejki priorytetowej
opartej o kopiec Fibonacciego (dla kolejki opartej o kopiec binarny mielibyśmy
O(V*E*log V), co dla grafów gęstych jest nieefektywne). Dla grafów gęstych E ~
V^2 złożoność obu implementacji (tj. przedstawionej i wzorcowej) jest jednakowa.
'''


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
        s, t = 0, 0
        processed = [False for _ in range(len(graph))]
        weightSum = [0 for _ in range(len(graph))]

        for _ in range(len(graph)):
            u = weightSum.index(max(weightSum))
            if not processed[u]:
                s, t = u, s
                weightSum[u] = 0
                processed[u] = True
                for v in range(len(graph)):
                    if not processed[v]:
                        weightSum[v] += graph[u][v]
        tmp_ans = sum(graph[s])
        mergeVertices(graph, s, t)

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
        graph = convert_graph(V, L)

        start = time.time()
        ans = StoerWagner(graph)
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
