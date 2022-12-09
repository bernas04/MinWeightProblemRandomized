import random
import networkx as nx
import matplotlib.pyplot as plt


class Graph:

    def __init__(self, nodes, edges, listEdges=[]):
        self.nodes = nodes
        self.edges = edges

        self.nodesList = [int(i) for i in range(self.nodes)]
        self.edgeWeight = {}

        self.nodesMerged = {str(i):str(i) for i in range(self.nodes)}

        if listEdges == []:
            self.listEdges, self.adjencyList = self.build_edges(edges)
        else:
            listFinal = []
            for i in listEdges:
                no1, no2 = i.split(" ")
                listFinal.append(tuple(sorted((no1, no2))))

            self.listEdges = listFinal
            self.adjencyList = self.buildAdjencyList(self.listEdges)

        for i in self.listEdges:
            self.edgeWeight[i] = random.randint(1,15)

        self.nxGraph = nx.Graph()

        

    """ def fromAdjencyListToEdges(self):
        edges = []
        for node in self.adjencyList.keys():
            for neighbour in self.adjencyList[node]:
                edges.append(tuple(sorted((node, neighbour)))) """


        

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

                edge_sorted = tuple(sorted((node1, node2)))
            
                if edge_sorted not in edges:
                    edges.append(edge_sorted)
                    i+=1
            
            isConnex, adjencyList = self.connexGraph(self.nodes, edges)
        return edges, adjencyList


    def connexGraph(self, nodes, connections):
        """ Check if graph is connex """
        # {0: [1, 2, 3], 1: [0, 2], 2: [0, 1, 3], 3: [0, 2]}
        adjencyList = self.buildAdjencyList(connections)
        
        if len(adjencyList) != nodes:
            return (False, None)
        
        postitionBoolean = [False for i in range(nodes)]
        stack = []

        stack.append('0')

        while stack:
            node = stack.pop()
            postitionBoolean[int(node)] = True
            neighbours = adjencyList[node]
            [stack.append(i) for i in neighbours if not postitionBoolean[int(i)]]
        
        if postitionBoolean == [True for i in range(nodes)]:
            return (True, adjencyList)
        else:
            return (False, None)

    
    def buildAdjencyList(self, listEdges) -> dict:
        """Create the adjency list of the graph in the form of a dictionary
            ex: {0: [1, 2, 3], 1: [0, 2], 2: [0, 1, 3], 3: [0, 2]}"""

        # listEdges = [(0, 1), (0, 2), (0, 3), (1, 2), (2, 3)]
        tmp = {}
        for edge_tuple in listEdges:

            node1, node2 = edge_tuple
            node1 = str(node1)
            node2 = str(node2)

            if node1 not in tmp:
                tmp[node1] = [node2]
            else:
                tmp[node1].append(node2)

            if node2 not in tmp:
                tmp[node2] = [node1]
            else:
                tmp[node2].append(node1)
            
        return tmp


  
            
    def drawGraph(self, fileName):
        """Draw the graph using the networkx library"""

        for tuple_edge in self.listEdges:
            node1, node2 = tuple_edge
            self.nxGraph.add_edge(node1, node2, weight=self.edgeWeight[tuple_edge])

        
        edge_labels = nx.get_edge_attributes(self.nxGraph, "weight")

        nx.draw(self.nxGraph, with_labels=True)
        
        plt.savefig(fileName)
        plt.clf()


    def mergeNodes(self, edge):
        """Merge the nodes of an edge"""

        # remover a aresta da lista de arestas
        self.listEdges.remove(edge)
        # nó inicial e nó final da aresta
        node_inicial, node_final = edge
        
        node1 = self.nodesMerged[str(node_inicial)]
        node2 = self.nodesMerged[str(node_final)]

        if node1 == node2:
            return

        # ir buscar as conexões de cada nó
        startingNode = self.adjencyList[node1]
        endingNode = self.adjencyList[node2]


        # remover da lista de adjacências os nós que vão ser unidos
        for i in startingNode:
            if i == node2:
                startingNode.remove(i)

        for i in endingNode:
            if i == node1:
                endingNode.remove(i)
        

        allNodes = startingNode + endingNode

        # criar uma nova key
        newKey = str(node1)+":"+str(node2)

        eachNode = newKey.split(":")
        for i in eachNode:
            if i in allNodes:
                allNodes.remove(i)


        # dar update ao dicionário
        self.adjencyList[newKey] = allNodes
        if node1!=node2:
            del self.adjencyList[node1]
        del self.adjencyList[node2]
        
        # guardar neste dicionario o nó e qual o novo nó que ele representa
        self.updateMergedNodes(newKey)

        self.nodes-=1
        
        

    def updateMergedNodes(self, newKey):
        """Update the nodes merged dictionary"""
        allNodes = newKey.split(":")
        for i in allNodes:
            self.nodesMerged[i] = newKey

        


class KargerAlgorithm:
    """Implementation of the Karger algorithm to find the minimum cut of a graph"""

    def __init__(self, graph):
        self.graph = graph


    def kargerMinCut(self, graph):
        """Find the minimum cut of a graph using the Karger algorithm"""
        while graph.nodes > 2:
            # choose a random edge
            try:
                edge = random.choice(graph.listEdges)
            except:
                break
            # merge the nodes of the edge
            graph.mergeNodes(edge)

        cost = 0
        for i in graph.listEdges:
            cost += graph.edgeWeight[i]

        return graph.listEdges, cost
        

        