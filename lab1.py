import os, time
from dimacs import *
    
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
    
#-------------------------------------------------

directory = 'graphs'
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
    print(ans)
    print("%.4f" % T, "s")
    
    if ans==int(words[-1]) and T<=1 : print("OK!")
    elif T>1: print("Za wolno!")
    else: print("Błąd!")
    
    print("-----------------")

#-------------------------------------------------
