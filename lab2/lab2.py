import os, time
from dimacs import *
from collections import deque 

def convert_graph(V,L):
    G = [[0 for _ in range(V)] for _ in range(V)]
    for u,v,w in L:
        G[u-1][v-1] = w
    
    return G

def BFS(G,root,end):
    explored = [False]*len(G)
    parent = [-1]*len(G)
    Q = deque()
    explored[root] = True
    Q.append(root)
    
    while Q:
        v = Q.popleft()
        for u in range(len(G)):
            if G[v][u]!=0 and not explored[u]:
                explored[u] = True
                parent[u] = v
                Q.append(u)
    
    u = end
    path = []
    while parent[u]!=-1:
        path.append(u)
        u = parent[u]
    if len(path)>0: path.append(u)
    return path[::-1]
    
def EdmondsKarp(C,s,t):
    n = len(C)

    f = [[0 for _ in range(n)] for _ in range(n)] # funkcja przepływu
    r = [[0 for _ in range(n)] for _ in range(n)] # sieć residualna
    for u in range(n):
        for v in range(n):
            r[u][v] = C[u][v]

    path = True
    while path:
        p = BFS(r,s,t) # ścieżka powiększająca
        if len(p)==0: path = False
        else:
            a = float('inf')
            for i in range(len(p)-1):
                v,u = p[i],p[i+1]
                a = min(a,r[v][u])
            for i in range(len(p)-1):
                v,u = p[i], p[i+1]
                f[v][u] = f[v][u] + a
                f[u][v] = f[u][v] - a
                r[v][u] = C[v][u] - f[v][u]
                r[u][v] = C[u][v] - f[u][v]

    max_flow = sum(f[s])
    for u in range(len(f)):
        for v in range(len(f)):
            print(f[u][v], ' ', end="")
        print("")
    return max_flow

# Program testujący
def test():

    total_time = 0
    Num_correct = 0
    Num = 0
    directory = 'flow'
    max_time = 1
    for filename in os.listdir(directory):
        
        f = os.path.join(directory, filename)
        if (f=='flow\simple'):
            with open( f ) as F:
                first_line = F.readline()
                words = first_line.split()
            V, L = loadWeightedGraph( f )
            
            start = time.time()
            ans = EdmondsKarp( convert_graph(V,L),0,V-1 )
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

