# from data import runtests


def my_solve(N, M, K, base, wages, eq_cost):

    events = [set() for _ in range(N)]
    ans = []
    TotalCost = 0
    costs = {
        i: [(j, base[i - 1][0] + eq_cost[j - 1] + wage) for j, wage in wages[i - 1]]
        for i in range(1, N + 1)
    }
    print(costs)
    while len(ans) < K:
        i = min(costs, key=lambda x: min(costs[x], key=lambda y: y[1])[1])
        event = min(costs[i], key=lambda x: x[1])
        events[i - 1].add(event[0])
        ans.append((event, i))
        TotalCost += event[1]
        costs[i] = []
        if len(events[i - 1]) < len(base[i - 1]):
            for j, wage in wages[i - 1]:
                if j not in events[i - 1]:
                    costs[i].append(
                        (
                            j,
                            wage
                            + eq_cost[j - 1]
                            + base[i - 1][len(events[i - 1])]
                            - base[i - 1][len(events[i - 1]) - 1],
                        )
                    )
        if len(costs[i]) == 0:
            del costs[i]
        # print(events)
        # print(TotalCost)
        # print(costs)
    print(ans)
    return TotalCost


def lcg(seed):
    a = 1103515245
    a = 69069
    c = 12345
    m = 2**31
    while True:
        yield seed ^ (seed >> 16)
        seed = (a * seed + c) % m


generator = lcg(314159265)
myrand = lambda a, b: a + next(generator) % (b - 1)


def random_cost_list(cap, step_min, step_max):
    c = 0
    v = 0
    a = 0
    costs = []
    for _ in range(cap):
        a = myrand(step_min, step_max)
        v += a
        c += v
        costs.append(c)
    return costs


def make_dense(N, M, K, cap_min, cap_max, step_min, step_max, cmin, cmax, eqmin, eqmax):

    base = [
        random_cost_list(myrand(cap_min, cap_max), step_min, step_max) for _ in range(N)
    ]

    wages = []
    for _ in range(N):
        current = []
        for j in range(1, M + 1):
            cost = myrand(cmin, cmax)
            current.append((j, cost))
        wages.append(current)

    eq_cost = [myrand(eqmin, eqmax) for _ in range(M)]

    return [N, M, K, base, wages, eq_cost]


def make_sparse(
    N, M, K, conn, cap_min, cap_max, step_min, step_max, cmin, cmax, eqmin, eqmax
):
    def flip():
        return myrand(0, 1000) / 1000.0 < conn

    base = [
        random_cost_list(myrand(cap_min, cap_max), step_min, step_max) for _ in range(N)
    ]

    wages = []
    for _ in range(N):
        current = []
        for j in range(1, M + 1):
            if flip():
                cost = myrand(cmin, cmax)
                current.append((j, cost))
        wages.append(current)

    eq_cost = [myrand(eqmin, eqmax) for _ in range(M)]

    return [N, M, K, base, wages, eq_cost]


"""
{"arg": make_dense(5, 6, 15, 3, 5, 4, 7, 10, 30, 5, 20),
"hint": 602
},
{"arg": make_dense(40, 30, 300, 5, 10, 4, 10, 10, 30, 5, 18),
"hint": 17869
},
{"arg": make_sparse(20, 30, 13, 0.2, 5, 10, 4, 10, 10, 30, 5, 18),
"hint": 422
},
{"arg": make_sparse(200, 100, 280, 0.1, 5, 10, 4, 10, 10, 30, 5, 18),
"hint": 9271
},"""

N, M, K, base, wages, eq_cost = tuple(
    make_sparse(20, 30, 13, 0.2, 5, 10, 4, 10, 10, 30, 5, 18)
)

print(N, M, K)
print("==============")
i = 1
for l in base:
    print("%.0f:" % i, l)
    i += 1
print("==============")
i = 1
for l in wages:
    print("%.0f:" % i, l)
    i += 1
print("==============")
print(eq_cost)
print("==============")
print("==============")
print(my_solve(N, M, K, base, wages, eq_cost))
# runtests(my_solve)
