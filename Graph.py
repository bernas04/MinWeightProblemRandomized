import random
import networkx as nx
import matplotlib.pyplot as plt


class Graph:

    def __init__(self, nodes, edges, listEdges=[]):
        self.nodes = nodes
        self.edges = edges

        if listEdges == []:
            self.listEdges = self.build_edges(edges)
        else:
            self.listEdges = listEdges

        self.nxGraph = nx.Graph()

        self.adjencyList = self.buildAdjencyList(self.listEdges)
        self.adjencyMatrix = self.buildMatrix(self.listEdges)  
        self.drawGraph()



        

    def build_edges(self, n_edges):
        """Build a list of edges in order to create a connex graph"""
        isConnex = False
        while not isConnex:
            edges = []
            i=0
            while i < n_edges:

                node1 = random.randint(0, self.nodes-1)
                node2 = random.randint(0, self.nodes-1)
                while (node1 == node2):
                    node2 = random.randint(0, self.nodes-1)

                if str(node1) + " " + str(node2) not in edges and str(node2) + " " + str(node1) not in edges:
                    edges.append(str(node1) + " " + str(node2))
                    i+=1
            
            isConnex = self.connexGraph(self.nodes, edges)
        return edges


    def connexGraph(self, nodes, connections):
        """ Check if graph is connex """
        visited = [False for i in range(nodes)]
        queue = []
        queue.append(0)
        visited[0] = True

        while queue:
            s = queue.pop(0)
            for i in connections:
                if str(s) in i:
                    tmp = i.split(" ")
                    tmp.remove(str(s))
                    if not visited[int(tmp[0])]:
                        queue.append(int(tmp[0]))
                        visited[int(tmp[0])] = True

        for i in visited:
            if not i:
                return False
        return True
        

    
    def buildAdjencyList(self, listEdges) -> dict:
        """Create the adjency list of the graph in the form of a dictionary
            ex: {0: [1, 2, 3], 1: [0, 2], 2: [0, 1, 3], 3: [0, 2]}"""

        tmp = {}
        for i in listEdges:
            list_i = i.split(" ")

            tmp_tpl = tuple(sorted(tuple(list_i)))

            if (tmp_tpl[0] == tmp_tpl[1]):
                raise Exception("ERROR: self loop")
                
            
            if tmp_tpl[0] not in tmp.keys():
                tmp[tmp_tpl[0]] = [tmp_tpl[1]]
            else:
                tmp[tmp_tpl[0]].append(tmp_tpl[1])
        return tmp


    def buildMatrix(self, listEdges) -> list:
        """Create the adjency matrix of the graph in the form of a list of lists
            ex: [[0, 1, 1, 1], [1, 0, 1, 0], [1, 1, 0, 1], [1, 0, 1, 0]]"""
        tmp = [[0 for i in range(self.nodes)] for j in range(self.nodes)]
        
        for i in listEdges:
            list_i = i.split(" ")

            firstNode, secondNode = tuple(list_i)

            firstNode = int(firstNode)
            secondNode = int(secondNode)


            # calcular aleatoriamente o peso associado à aresta
            weight = random.randint(1, 15)

            # completar o nxGraph
            self.nxGraph.add_edge(firstNode, secondNode, weight=weight)


            if tmp[int(firstNode)][int(secondNode)] == 0 and tmp[int(secondNode)][int(firstNode)] == 0:
                tmp[firstNode][secondNode] = weight
                tmp[secondNode][firstNode] = weight
            else:
                tmp[firstNode][secondNode] += weight
                tmp[secondNode][firstNode] += weight

        return tmp
            
    def drawGraph(self):
        """Draw the graph using the networkx library"""
        
        edge_labels = nx.get_edge_attributes(self.nxGraph, "weight")

        nx.draw(self.nxGraph, with_labels=True)
        
        print(self.nxGraph.nodes)
        pos = nx.circular_layout(self.nxGraph)
        
        nx.draw_networkx_edge_labels(self.nxGraph, pos, edge_labels)
        plt.show()
        

        
        

        