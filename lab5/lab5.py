import os
import time
from dimacs import *


def LexBFS(Graph: list[set()]) -> list:
    sets = [{u for u in range(len(Graph))}]
    sequence = []

    while len(sets) > 0:
        u = sets[-1].pop()
        T = []
        for X in sets:
            Y, K = X & Graph[u], X - Graph[u]
            T.append(K) if len(K) > 0 else None  # O(1)
            T.append(Y) if len(Y) > 0 else None  # O(1)
        sets = T
        sequence.append(u)

    return sequence


def checkPEO(Graph: list[set()], sequence: list) -> bool:
    RN = [set() for _ in range(len(Graph))]
    parent = [None for _ in range(len(Graph))]

    for u in range(len(Graph)):
        last = None
        for v in sequence:
            if u == v:
                break
            elif v in Graph[u]:
                RN[u].add(v)
                last = v
            else:
                continue
        parent[u] = last

    for u in range(len(Graph)):
        if parent[u] != None and not (RN[u] - {parent[u]} <= RN[parent[u]]):
            return False

    return True


# Zadanie 1


def isChordal(Graph: list[set()]) -> bool:
    return checkPEO(Graph, LexBFS(Graph))


# Zadanie 2


def maxClique(Graph: list[set()]) -> int:
    sequence = LexBFS(Graph)
    RN = [set() for _ in range(len(Graph))]
    for u in range(len(Graph)):
        for v in sequence:
            if u == v:
                break
            elif v in Graph[u]:
                RN[u].add(v)
            else:
                continue
    K = 0
    for u in range(len(Graph)):
        K = max(K, len(RN[u]) + 1)

    return K


# Zadanie 3


def chromaticNumber(Graph: list[set()]) -> int:
    sequence = LexBFS(Graph)
    color = [0 for _ in range(len(Graph))]
    maxColor = 0
    for u in sequence:
        used = {color[v] for v in Graph[u]}
        S = set(color) - used - {0}
        if len(S) > 0:
            c = min(list(S))
        else:
            maxColor += 1
            c = maxColor
        color[u] = c

    return maxColor


# Zadanie 4


def minCover(Graph: list[set()]) -> int:
    sequence = LexBFS(Graph)[::-1]
    I = set()

    for u in sequence:
        if len(I & Graph[u]) == 0:
            I.add(u)

    return len(Graph) - len(I)


# Testy


def test():
    def convertGraph(V, L):
        Graph = [set() for _ in range(V)]
        for u, v, w in L:
            Graph[u - 1].add(v - 1)
            Graph[v - 1].add(u - 1)
        return Graph

    numOfEx = input("Podaj numer zadania: ")

    match numOfEx:
        case "1":
            func = isChordal
            directory = "chordal"
            print("###### ZADANIE 1 ######")
        case "2":
            func = maxClique
            directory = "maxclique"
            print("###### ZADANIE 2 ######")
        case "3":
            func = chromaticNumber
            directory = "coloring"
            print("###### ZADANIE 3 ######")
        case "4":
            func = minCover
            directory = "vcover"
            print("###### ZADANIE 4 ######")
        case _:
            print("Nieprawidłowa komenda. Dostępne komendy: 1, 2, 3, 4")
            return None

    Num_correct = 0
    Num = 0
    max_time = 100
    for filename in os.listdir(directory):

        f = os.path.join(directory, filename)

        with open(f) as F:
            first_line = F.readline()
            words = first_line.split()
        V, L = loadWeightedGraph(f)

        start = time.time()
        ans = func(convertGraph(V, L))
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
    print("---------------------------")
    print("###########################")
    print("---------------------------")


test()
