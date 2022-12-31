#  Projekt 1
#  Author: Bartosz Hanc

from data import runtests


def solve(N, M, K, base, wages, eq_cost):  # O(M*N*K + N*M*log(M))
    C = [[] for _ in range(N)]

    for i in range(N):
        O = sorted([wages[i][j][1] + eq_cost[wages[i][j][0]-1]
                   for j in range(len(wages[i]))])
        cost = 0
        for j in range(min(len(base[i]), len(O))):
            cost += O[j]
            C[i].append((j+1, cost + base[i][j]))

    dp = [[[float('inf') for _ in range(M+1)]
           for _ in range(N+1)] for _ in range(K+1)]

    for k in range(K+1):
        for wiz in range(N, -1, -1):
            for show in range(M, -1, -1):
                if k <= 0:
                    dp[k][wiz][show] = 0
                elif wiz >= N or show >= len(C[wiz]):
                    dp[k][wiz][show] = float('inf')
                else:
                    dp[k][wiz][show] = min(
                        dp[k-C[wiz][show][0]][wiz+1][0] + C[wiz][show][1],
                        dp[k][wiz][show+1],
                        dp[k][wiz+1][0]
                    )

    return min(min(dp[K], key=lambda x: min(x)))


runtests(solve)
