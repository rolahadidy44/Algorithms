import heapq

class Graph:
    def __init__(self,V):
        self.V=V
        self.adj=[[] for _ in range(V)]
        
        def add_edge(slef,u,v,w):
            self.adj[u].append((u,w))
            self.adj[v].append((u,w))
            
        def prim_mst(self):
            pq=[]
            src=0
            key=[float('inf')]*self.V
            parent=[-1] *self.V
            
            is_in_mst=[False] *self,V
    pass
            
            
            
    