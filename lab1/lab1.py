import os, time
from dimacs import *

''' Metoda 1
Korzystamy ze struktury find-union. Najpierw sortujemy wszystkie krawędzie malejąco
względem ich wag. Następnie konstruujemy drzewo rozpinające korzystając z tak posortowanych krawędzi
do momentu kiedy wierzchołki s i t są połączone. Wynikiem algorytmu jest wówczas waga ostatniej 
wykorzystanej krawędzi. Złożoność algorytmu to O(E log V).
'''

class Node:
    def __init__(self, val):
        self.val = val
        self.parent = self
        self.rank = 0
        
def find( x ):
    if x.parent!=x:
        x.parent = find( x.parent )
    return x.parent
    
def union(x, y):
    x, y = find(x), find(y)
    if x==y: return
    if x.rank>y.rank:
        y.parent = x
    else:
        x.parent = y
        if x.rank==y.rank:
            y.rank+=1
            
def Kruskal( G, V, s, t ): # G w postaci krawędziowej (u,v,weight)
    vertices, F = [Node(v) for v in range(V)], []
    for u,v,weight in G:
        F.append((vertices[u-1],vertices[v-1],weight))
    F.sort(key=lambda x: x[2])
    F = F[::-1]

    i = 0
    min_weight = F[0][2]
    while find(vertices[s])!=find(vertices[t]):
        u, v, weight = F[i]
        if find(u)!=find(v):
            union(u,v)
            min_weight = weight
        i+=1
    return min_weight
    

# Program testujący
def test():

    total_time = 0
    Num_correct = 0
    Num = 0
    directory = 'graphs'
    max_time = 1
    for filename in os.listdir(directory):
        
        f = os.path.join(directory, filename)
        with open( f ) as F:
            first_line = F.readline()
            words = first_line.split()
        V, L = loadWeightedGraph( f )
        
        start = time.time()
        ans = Kruskal( L, V, 0, 1 )
        end = time.time()
        T = end -start
        print(f)
        print("Oczekiwany wynik:", int(words[-1]))
        
        if ans==int(words[-1]) and T<=max_time : 
            print("Wynik:", ans, "|", "%.2f" % T, "s","|","OK!")
            Num_correct += 1
            
        elif T>max_time: print("Wynik:", ans, "|", "%.4f" % T, "s", "|", "Za wolno!")
            
        else: print("Wynik:", ans, "|", "%.4f" % T, "s","|","Błąd!")
        
        Num += 1
        
        print("-----------------")
    
    print(Num_correct, "/", Num)
    if Num_correct==Num: print("OK!")
    else: print("Błędy!")

test()