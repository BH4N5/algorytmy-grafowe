from data import runtests
"""
Bartosz Hanc | Projekt 1: Jarmark

Idea rozwiązania opiera się na zachłannym wyborze najtańszego dostępnego pokazu.
Obliczenie możemy reprezentować na grafie jako konstruowanie ścieżki o długości
K i minimalnej sumie wag krawędzi (każda krawędź reprezentuje wybrany pokaz, a
jej waga -- koszt pokazu). W każdym kroku budowy ścieżki wybieramy zachłannie
pokaz o minimalnym koszcie i aktualizujemy listę dostępnych pokazów (wraz z ich
kosztami) uwzględniając przyrost wynagrodzenia bazowego.

Korzystając z listy setów przechowujących dla każdego sztukmistrza indeksy
wybranych pokazów wykonywanych przez danego sztukmistrza złożoność czasową
działania algorytmu można sprowadzić do O(N*M+K*N+K*M). Istotnie aktualizacja
listy dostępnych pokazów wraz z kosztami wymaga maksymalnie O(M) operacji, gdyż
wystarczy przechowywać i zaktualizować najtańszy dostępny pokaz dla
sztukmistrza, którego pokaz wybraliśmy, a sprawdzenie czy dany pokaz nie został
już wybrany wykonujemy korzystając z setu w O(1). Znalezienie najtańszego pokazu
wymaga O(N) operacji, gdyż dla każdego sztukmistrza przechowujemy aktualnie
najtańszy oferowany pokaz. Potrzebujemy więc O(N*M) operacji do stworzenia listy
początkowo najtańszych pokazów oferowanych przez każego sztukmistrza, a
następnie K razy znajdujemy najtańszy pokaz i aktualizujemy listę pokazów, co
daje całkowitą złożoność O(N*M + K*(N + M)).
"""


def my_solve(N, M, K, base, wages, eq_cost):

    TotalCost = 0
    ShowsChosen = [set() for _ in range(N)]
    CheapestShow = [(float('inf'), float('inf')) for _ in range(N)]

    for artist in range(N):
        for j, wage in wages[artist]:
            cost = wage + eq_cost[j-1] + base[artist][0]
            CheapestShow[artist] = min(CheapestShow[artist], (cost, j))

    for _ in range(K):
        artist = CheapestShow.index(min(CheapestShow, key=lambda x: x[0]))
        cost, show = CheapestShow[artist]

        TotalCost += cost
        ShowsChosen[artist].add(show)
        CheapestShow[artist] = (float('inf'), float('inf'))

        if len(ShowsChosen[artist]) < len(base[artist]):
            for j, wage in wages[artist]:
                if j not in ShowsChosen[artist]:
                    k = len(ShowsChosen[artist])
                    baseIncr = base[artist][k]-base[artist][k-1]
                    cost = wage + eq_cost[j-1] + baseIncr
                    CheapestShow[artist] = min(
                        CheapestShow[artist], (cost, j))

    return TotalCost


runtests(my_solve)
