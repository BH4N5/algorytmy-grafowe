# Author: Bartosz Hanc

from data import runtests


def my_solve(N, channels):  # O(N log N + E)
    d = [0 for _ in range(N)]
    for u, v in channels:
        d[u-1] += 1
        d[v-1] += 1

    d.sort(key=lambda x: -x)

    m = 0
    for i in range(N):
        m = i if d[i] > i else m

    return m+1 if sum(d[:m+1]) == m*(m+1) + sum(d[m+1:]) else None


runtests(my_solve)
