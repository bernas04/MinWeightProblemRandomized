import sys, getopt, time
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
    contador=0
    # para cada ficheiro, ler o grafo e executar o algoritmo
    for file in files:
        
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
        f.close()

        tmp_conn = [i.replace("\n", "") for i in connections]


        if not os.path.exists("Solution"):
            os.makedirs("Solution")
        os.chdir("Solution")
        f = open(f"G(N{nodes}, E{edges}).txt", "w")

        allMinCut = []
        allTime = []
        for i in range(10):
            start = time.time()
            # criar o grafo
            print(f">>{contador}: {file}", end="\r")

            graph = Graph(nodes=nodes, edges=edges, listEdges=tmp_conn)
            contador+=1
            alg = KargerAlgorithm(graph)
            edgesToCut, minCut = alg.kargerMinCut(graph)
            end = time.time() - start
            f.write(f">> G{i}(N{nodes}, E{edges}) - cost: {minCut}, edges: {edgesToCut}, time: {end}\n")
            allMinCut.append(minCut)
            allTime.append(end)
        
        f.write(f"MinCut: {str(min(allMinCut))}, time: {str(sum(allTime)/len(allTime))}")
        f.write("\n")
        f.close()
        os.chdir("..")




        
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

                f = open(f"G(N{nodesNumber}, E{edgesNumber}).txt", "w")
                allMinCut = []
                allTime = []
                for m in range(10):
                    start = time.time()
                    contador+=1

                    print(f">>G{contador}(N{nodesNumber}, E{edgesNumber})", end="\r")
                    graph = Graph(nodes=nodesNumber, edges=edgesNumber)
                    graph.drawGraph(f"G{contador}(N{nodesNumber}, E{edgesNumber})")

                    alg = KargerAlgorithm(graph)

                    edgesToCut, minCut = alg.kargerMinCut(graph)

                    allMinCut.append(minCut)
                    end = time.time() - start
                    allTime.append(end)
                    f.write(f">> G{m}(N{nodesNumber}, E{edgesNumber}) - cost: {minCut}, edges: {edgesToCut}, time: {end}\n")
                    
                f.write(f"MinCut: {str(min(allMinCut))}, time: {str(sum(allTime)/len(allTime))}")
                f.write("\n")
                f.close()


    os.chdir("..")

            







if __name__ == "__main__":
    main(sys.argv[1:])
