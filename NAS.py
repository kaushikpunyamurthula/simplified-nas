from collections import defaultdict

intermediateAirports = ['ATL', 'BOS', 'DEN', 'IAD', 'ORD', 'PHX', 'SEA', 'SFO']
acceptedAirports = {'LAX': 0, 'ATL': 1, 'BOS': 25, 'DEN': 49, 'IAD': 73, 'ORD': 97, 'PHX': 121, 'SEA': 145, 'SFO': 169, 'JFK': 193}

airportNodes = ['LAX']
for i in intermediateAirports:
    for j in range(0, 24):
        airportNodes.append(i+"_"+str(j))
airportNodes.append('JFK')

timeConversionMap = {6: 0, 7: 1, 8: 2, 9: 3, 10: 4, 11: 5, 12: 6, 13: 7, 14: 8, 15: 9, 16: 10, 17: 11, 18: 12, 19: 13, 20: 14, 21: 15, 22: 16, 23: 17, 24: 18, 0: 18, 1: 19, 2: 20, 3: 21, 4: 22, 5: 23}

graph = []
for i in range(len(airportNodes)):
    if i not in [0, 192, 193]:
        start = i%24
        l = 194 - 24 + start - (i+1)
        graph.append([0]*(i+1) + [float("inf")] * (24 - start) + [0]*l)
    else:
        graph.append([0]*len(airportNodes))

def read_flight_data(filename):
    with open(filename, "r") as f:
        maxFlow = 0
        for i, line in enumerate(f.readlines()):
            source, destination, departure, arrival, capacity = line.split()
            sourceNode, destinationNode = None, None
            
            if destination == "LAX" or timeConversionMap[int(departure)] >  timeConversionMap[int(arrival)]:
                continue

            if source == "LAX" and destination == "JFK":
                maxFlow += int(capacity)
                continue

            sourceNode = sourceNode = source if source == "LAX" else source+ "_" + str(timeConversionMap[int(departure)])
            destinationNode = destinationNode = destination if destination == "JFK" else destination+ "_" + str(timeConversionMap[int(arrival)])

            graph[airportNodes.index(sourceNode)][airportNodes.index(destinationNode)]+= int(capacity)

        return maxFlow

direct_maxFlow = read_flight_data("flights.txt")
print(direct_maxFlow)

class Graph:

    def __init__(self, graph):
        self.graph = graph
        self. ROW = len(graph)


    # Using BFS as a searching algorithm 
    def BFS(self, s, t, parent):

        visited = [False] * (self.ROW)
        queue = []
        queue.append(s)
        visited[s] = True

        while queue:

            u = queue.pop(0)

            for ind, val in enumerate(self.graph[u]):
                if visited[ind] == False and val > 0:
                    queue.append(ind)
                    visited[ind] = True
                    parent[ind] = u

        return True if visited[t] else False

    # Applying fordfulkerson algorithm
    def ford_fulkerson(self, s, t):
        # source = acceptedAirports[s]
        # destination = acceptedAirports[t]
        parent = [-1] * (self.ROW)
        maxFlow = 0

        while self.BFS(s, t, parent):

            minPathFlow = float("inf")
            s = destination
            while(s != source):
                minPathFlow = min(minPathFlow, self.graph[parent[s]][s])
                s = parent[s]

            # Adding the path flows
            maxFlow += minPathFlow

            # Updating the residual values of edges
            v = destination
            while(v != source):
                u = parent[v]
                self.graph[u][v] -= minPathFlow
                self.graph[v][u] += minPathFlow
                v = parent[v]

        return maxFlow

g = Graph(graph)

source = 0
destination = 193

# print(int(g.ford_fulkerson(source, destination)))

intermediate_nodes_maxFlow = int(g.ford_fulkerson(source, destination))
print(intermediate_nodes_maxFlow)

maxFlow = direct_maxFlow + intermediate_nodes_maxFlow

print ("Maximum Passengers that can travel from Los Angeles(LAX) to New York (JFK) between 6:00 AM present day to 5:59 AM the following day is: \n", maxFlow)