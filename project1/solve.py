from data import runtests


def my_solve(N, M, K, base, wages, eq_cost):  # Złożoność pesymistyczna O(N*M*K)

    ShowsChosen = [set() for _ in range(N)]
    ShowsAvailable = {artist: [(j, base[artist - 1][0] + eq_cost[j - 1] + wage)
                               for j, wage in wages[artist - 1]] for artist in range(1, N + 1)}
    TotalCost = 0
    NumOfShows = 0

    while NumOfShows < K:
        artist = min(ShowsAvailable, key=lambda x: min(
            ShowsAvailable[x], key=lambda y: y[1])[1],)
        show, cost = min(ShowsAvailable[artist], key=lambda x: x[1])

        ShowsChosen[artist - 1].add(show)
        NumOfShows += 1
        TotalCost += cost
        ShowsAvailable[artist] = []

        if len(ShowsChosen[artist - 1]) < len(base[artist - 1]):
            for j, wage in wages[artist - 1]:
                if j not in ShowsChosen[artist - 1]:
                    ShowsAvailable[artist].append((j, wage + eq_cost[j - 1] + base[artist - 1][len(
                        ShowsChosen[artist - 1])] - base[artist - 1][len(ShowsChosen[artist - 1]) - 1], ))

        if len(ShowsAvailable[artist]) == 0:
            del ShowsAvailable[artist]

    return TotalCost


runtests(my_solve)
