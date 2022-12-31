# Projekt 1
# Author: Bartosz Hanc

from data import runtests


def rek(MEM, C, N, k, wiz=0, show=0):
    if k <= 0:
        return 0
    if wiz >= N or show >= len(C[wiz]):
        return float('inf')
    if MEM[k][wiz][show] != None:
        return MEM[k][wiz][show]

    x = min(rek(MEM, C, N, k-C[wiz][show][0], wiz+1, 0) + C[wiz][show][1],
            rek(MEM, C, N, k, wiz, show+1),
            rek(MEM, C, N, k, wiz+1, 0))
    MEM[k][wiz][show] = x
    return x


def solve(N, M, K, base, wages, eq_cost):  # O(M*N*K + N*M*log(M))
    C = [[] for _ in range(N)]

    for i in range(N):
        O = sorted([wages[i][j][1] + eq_cost[wages[i][j][0]-1]
                   for j in range(len(wages[i]))])
        cost = 0
        for j in range(min(len(base[i]), len(O))):
            cost += O[j]
            C[i].append((j+1, cost + base[i][j]))

    MEM = [[[None for _ in range(M)] for _ in range(N)] for _ in range(K+1)]

    return rek(MEM, C, N, K)


runtests(solve)
