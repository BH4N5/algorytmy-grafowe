# Project 2
# Author: Bartosz Hanc

from data import runtests


def solve(N: int, channels) -> (int | None):  # O(E + N log N)
    d = [0 for _ in range(N)]
    for u, v in channels:
        d[u-1] += 1
        d[v-1] += 1

    d.sort(key=lambda x: -x)

    m = 0
    while d[m] > m:
        m += 1
    m -= 1

    return m+1 if sum(d[:m+1]) == m*(m+1) + sum(d[m+1:]) else None


runtests(solve)
