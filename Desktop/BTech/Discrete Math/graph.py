
from collections import deque

class Graph:
    # args => start = starting node, target = target node, directed = directed/undirected
    def __init__(self, start=None, target=None, directed= False) -> None:
        self.start = start; 
        self.target = target; 
        self.directed = directed
        self.weighted = False
        self.algoID = None
        self.edges = list(); 
        self.vertices = list()
        self.adjList = dict(); 

    #Depth First Search Algorithm 
    def dfs(self):
        self.algoID ='DFS'
        pass

    #Breadth First Search Algorithm -> find the shortest path of non-weighted graph
    def bfs(self):
        self.algoID = 'BFS'
        if self.weighted: print("Error: BFS algorithm only works for non-weighted graph!"); return
        else: self.dijkstra()

    
    #Dijkstra's Algorithm -> find the shortest path of weighted graph
    def dijkstra(self):
        if not self.weighted and self.algoID != 'BFS': 
            print("Error: Dijkstra's algorithm only works for weighted graph!")
            return
        
        self.algoID = 'DJK'
        visited = {self.start:str(0)}; 
        queue = deque([self.start])
        
        while queue:
            node = queue.popleft()
            for k,v in node.next.items():
                if k not in visited and k is not self.start:
                    queue.append(k)
                    nodevalue = int(''.join([val for val in visited[node] if val.isdigit()]))
                    visited.update({k:f'{v+nodevalue}{node}'})
                    continue
                if k in visited and k is not self.start:
                    value = int(''.join([val for val in visited[node] if val.isdigit()]))
                    prevalue = int(''.join([val for val in visited[k] if val.isdigit()]))
                    if v+value < prevalue: visited[k] = f'{v+value}{node}'

        if self.target:
            self.shortest_path(visited); 
        else: 
            self.spanning_trees(visited)

    #find the spanning trees of a graph using dijkrsta/bfs 
    def spanning_trees(self, visited:dict)->None:
        st = dict()
        while len(st.keys()) != len(visited.keys()):
            node = next(n for n in visited.keys() if n not in st.keys()); 
            adj = [f'{k}({v})' for k,v in visited.items() if any(c==node for c in v)]
            st.update({node:adj if len(adj)!= 0 else ['None']})       
        fmt = str()
        for k,v in st.items(): fmt += f"{k} =>  {' -> '.join(v)}\n"
        print(fmt)
        
    #get the shortest path using dijkrsta/bfs 
    def shortest_path(self, visited:dict)->None:
        sp = deque()
        node = next(k for k in visited if k == self.target); sp.appendleft(f'{node}({visited[node]})')
        while node is not str(self.start):
            node = next(k for k in visited[node] if k.isalpha())
            sp.appendleft(f'{node}({visited[node]})')
        print(' -> '.join(sp))
            
    def load_matrix(self, matrix:list, vertices:list)->None:
        edges = list()
        # self.weighted = any([[i for i in item if i>1] for item in vertices])
        data = dict(zip(vertices,[list(zip([v for v in vertices], [data for data in row])) for row in matrix]))
        for k in data:
            filtered = list(map(lambda x: list(x), (filter(lambda x: x[1] >=1, data[k]))))
            for i in filtered: 
                if filtered: i.insert(0,k); edges.append(i)
        self.load_edges(edges)

    
   #load edges list([a,b,wt]) in graph.                   
    def load_edges(self, edges:list)->None:
        for edge in edges:
            if len(edge)==2: edge.append(1)
            src, des, wt = edge
            src, des = self.assign_vertex(src), self.assign_vertex(des)
            if not self.directed: src.next.update({des:wt}); des.next.update({src:wt})
            else: src.next.update({des:wt}) 
            self.edges.append((src, des, wt))
        if any(e[2] for e in edges if e[2]>1): self.weighted = True
        self.update_adjacency_list()
    
    #create vertex or assign if already existing
    def assign_vertex(self, node)->object:
        if node not in self.vertices:
            node = Vertex(node)
            if node == self.start: self.start = node
            if node == self.target: self.target = node
            self.vertices.append(node)
        else:
            node = next((v for v in self.vertices if node == v))
        return node

    #load the adjacency list
    def update_adjacency_list(self)->None:
        for v in self.vertices:
            self.adjList.update({v:v.next})
    
    #print the graph i.e ajacency list
    def __repr__(self) -> str:
        formated = str()
        for k,v in self.adjList.items():
             formated += f'{k} -> {v}\n'
        return formated
    

# Vertex class: create vertex instance obj                 
class Vertex:
    def __init__(self, data) -> None:
        self.data = data 
        self.next = dict()

    #print vertex name
    def __repr__(self) -> str:
        return f'{self.data}'
    
    def __hash__(self) -> int:
        return hash(str(self.data))
    
    def __eq__(self, node) -> bool:
        return (self.data) == (str(node))
    





#Weighted edge loading 
edges = [['S','A', 3],
         ['S','E', 2],
         ['A','B', 3],
         ['E','F', 2], 
         ['E','I', 4],
         ['B','C', 2],
         ['C','D', 1],
         ['F','G', 2],
         ['G','H', 2], 
         ['I','J', 2],
         ['F','I', 1],
         ['J','K', 1],
         ['D','K', 3],
         ['H','K', 4]
         ]


# #Unweighted edge loading
# edges = [['S','A'],
#          ['S','E'],
#          ['A','B'],
#          ['E','F'], 
#          ['E','I'],
#          ['B','C'],
#          ['C','D'],
#          ['F','G'],
#          ['G','H'], 
#          ['I','J'],
#          ['F','I'],
#          ['J','K'],
#          ['D','K'],
#          ['H','K']
#          ]

vertices = ['A', 'B', 'C', 'D']

# Unweighted Adjency Matrix[i][i] where i = num of vertices.
matrix = [[0,1,0,1],
          [0,0,0,1],
          [0,1,0,1],
          [0,0,0,0]
        ]
        

graph = Graph('A')
graph.load_matrix(matrix, vertices)
graph.bfs()


