import sys, getopt
import os
from Graph import Graph, KargerAlgorithm




GRAPHS = 15
EDGES_PERCENTAGE = [0.125, 0.25, 0.50, 0.75]

def main(argv):

    folder=""
    try:
      opts, args = getopt.getopt(argv,"hf:",["folder="])
    except getopt.GetoptError:
        print('test.py -f <pathToFolder>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('test.py -f <pathToFolder>')
            sys.exit()
        elif opt in ("-f", "--folder"):
            folder = arg


    if folder !="":
        useTeacherGraphs(folder)
    else:
        generateRandomGraphs(GRAPHS)


def useTeacherGraphs(folder):
    os.chdir(folder)
        
    # abrir os ficheiros que interessam para a execução do programa
    files = [i for i in os.listdir() if i.startswith("SW") and i.endswith(
        "G.txt") and "DG" not in i and "DAG" not in i]
    
    # para cada ficheiro, ler o grafo e executar o algoritmo
    for file in files:
        if file != "SWtinyG.txt":
            continue
        f = open(file, "r")
        
        # ler a primeira linha: 0 se não é direcionado, 1 se é
        isDirected = int(f.readline())
        # ler a segunda linha: 0 se não tem pesos, 1 se tem
        existsWeight = int(f.readline())

        # Just to check that the file is correct
        assert isDirected == 0
        assert existsWeight == 0

        # ler a terceira linha: número de nós
        nodes = int(f.readline())
        # ler a quarta linha: número de arestas
        edges = int(f.readline())
        # ler as restantes linhas: as arestas
        connections = f.readlines()

        tmp_conn = [i.replace("\n", "") for i in connections]

        
        # criar o grafo
        graph = Graph(nodes=nodes, edges=edges, listEdges=tmp_conn)

        
def generateRandomGraphs(numberOfGraphs):
    if not os.path.exists("randomGraphs"):
        os.makedirs("randomGraphs")

    os.chdir("randomGraphs")

    contador=0
    for i in range(4, numberOfGraphs):

        nodesNumber = i
        maxEdges = (nodesNumber * (nodesNumber - 1)) / 2

        for j in EDGES_PERCENTAGE:
            edgesNumber = int(maxEdges * j)

            if edgesNumber >= nodesNumber-1:

                for m in range(10):
                    contador+=1
                    #print(f">>{m}: Karager Algorithm")

                    print(f">>G{contador}(N{nodesNumber}, E{edgesNumber})")
                    graph = Graph(nodes=nodesNumber, edges=edgesNumber)
                    graph.drawGraph(f"G{contador}(N{nodesNumber}, E{edgesNumber})")

                    alg = KargerAlgorithm(graph)

                    minCut = alg.kargerMinCut(graph)

                    print(">> ", minCut, "\n")


    os.chdir("..")

            







if __name__ == "__main__":
    main(sys.argv[1:])
