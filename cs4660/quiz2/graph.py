
from io import open
from operator import itemgetter

def construct_graph_from_file(graph, file_path):
    """
    TODO: read content from file_path, then add nodes and edges to graph object

    note that grpah object will be either of AdjacencyList, AdjacencyMatrix or ObjectOriented

    In example, you will need to do something similar to following:

    1. add number of nodes to graph first (first line)
    2. for each following line (from second line to last line), add them as edge to graph
    3. return the graph
    """
    openFile = open(file_path)
    readFile = openFile.read()
    splitReadFile = readFile.split("\n")
    lineSplit = [line.split(":") for line in splitReadFile if line != ""]
    
    numberOfNodes = int(lineSplit[0][0]) # first line = number of nodes

    for node in range(0, numberOfNodes): # create and add nodes to graph
        graph.add_node(Node(node) )

    for lineNumber in range(1, len(lineSplit) ): # start from 1 since first line is number of nodes
        fromNodeIndex = 0 # just in case
        toNodeIndex = 1 # this ever needs
        weightIndex = 2 # to change...
        
        fromNode = int(lineSplit[lineNumber][fromNodeIndex]) # cast to int; otherwise it's a str
        toNode = int(lineSplit[lineNumber][toNodeIndex])
        weight = int(lineSplit[lineNumber][weightIndex])
        
        graph.add_edge(Edge(Node(fromNode), Node(toNode), weight ) )

    openFile.close()
    
    return graph

class Node(object):
    """Node represents basic unit of graph"""
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return 'Node({})'.format(self.data)
    def __repr__(self):
        return 'Node({})'.format(self.data)

    def __eq__(self, other_node):
        if other_node == None:
            return False
        elif other_node.data == None: # added this as a helper
            return False
        return self.data == other_node.data
    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.data)

class Edge(object):
    """Edge represents basic unit of graph connecting between two edges"""
    def __init__(self, from_node, to_node, weight):
        self.from_node = from_node
        self.to_node = to_node
        self.weight = weight
    def __str__(self):
        return 'Edge(from {}, to {}, weight {})'.format(self.from_node, self.to_node, self.weight)
    def __repr__(self):
        return 'Edge(from {}, to {}, weight {})'.format(self.from_node, self.to_node, self.weight)

    def __eq__(self, other_node):
        if other_node == None:
            return False
        return self.from_node == other_node.from_node and self.to_node == other_node.to_node and self.weight == other_node.weight
    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.from_node, self.to_node, self.weight))


class AdjacencyList(object):
    """
    AdjacencyList is one of the graph representation which uses adjacency list to
    store nodes and edges
    """
    def __init__(self):
        # adjacencyList should be a dictonary of node to edges
        self.adjacency_list = {}

    def adjacent(self, node_1, node_2):
        if(node_1 in self.adjacency_list and node_2 in self.adjacency_list):
            for edge in self.adjacency_list[node_1]:
                if(edge.from_node == node_1 and edge.to_node == node_2):
                    return True
            return False # didn't find adjacent nodes, though they did exist in list
        else:
            return False

    def neighbors(self, node):
        neighborsList = []
        if(node in self.adjacency_list):
            for edge in self.adjacency_list[node]:
                neighborsList.append(edge.to_node) # populate list with neighbor nodes
            return neighborsList
        else:
            return []

    def add_node(self, node):
        if node in self.adjacency_list: # check if it already exists
            return False
        else:
            self.adjacency_list[node] = [] # empty list is initial state
            return True

    def remove_node(self, node):
        deleted = False
        if node in self.adjacency_list:
            del self.adjacency_list[node]
            deleted = True
        for line in self.adjacency_list:
            for edge in range(len(self.adjacency_list[line])):
                if self.adjacency_list[line][edge - 1].to_node == node:
                    del self.adjacency_list[line][edge]
                    deleted = True
        return deleted
        # need to search and remove edges that have the node too.........
        ## that means toNode...........
        # has to be a better way than double for loops

    def add_edge(self, edge):
        fromNode = edge.from_node
        toNode = edge.to_node
        if(fromNode in self.adjacency_list and toNode in self.adjacency_list):
            if(edge in self.adjacency_list[fromNode]): # checks of edge already exists in list
                return False
            else:
                self.adjacency_list[fromNode].append(edge)
                return True
        else: # one of the nodes doesn't exist in adj list
            return False

    def remove_edge(self, edge):
        fromNode = edge.from_node
        if(fromNode in self.adjacency_list):
            if(edge in self.adjacency_list[fromNode]):
                self.adjacency_list[fromNode].remove(edge)
                return True
            return False # edge doesn't exist in adj list, but fromNode does
        else:
            return False # fromNode doesn't exist in adj list

    def get_edge(self, node_1, node_2): # returns edge without checking/comparing weight
        if(node_1 in self.adjacency_list and node_2 in self.adjacency_list):
            for edge in self.adjacency_list[node_1]:
                if(edge.from_node == node_1 and edge.to_node == node_2):
                    return edge
            return None # didn't find adjacent nodes, though they did exist in list
        else:
            return None

    def distance(self, node_1, node_2):
        edge = self.get_edge(node_1, node_2)
        if(edge != None):
            return edge.weight
        else:
            return None

class AdjacencyMatrix(object):
    def __init__(self):
        # adjacency_matrix should be a two dimensions array of numbers that
        # represents how one node connects to another
        self.adjacency_matrix = []
        # in additional to the matrix, you will also need to store a list of Nodes
        # as separate list of nodes
        self.nodes = []

    def adjacent(self, node_1, node_2):
        if( (node_1 in self.nodes) and (node_2 in self.nodes) ):
            fromNodeIndex = self.nodes.index(node_1)
            toNodeIndex = self.nodes.index(node_2)
            if(self.adjacency_matrix[fromNodeIndex][toNodeIndex] > 0):
                return True
            else:
                return False
        else:
            return False

    def neighbors(self, node):
        if node in self.nodes:
            neighborsList = []
            index = self.nodes.index(node)
            #neighborsList = [Node(item) for item in self.adjacency_matrix[index] if item > 0]
            for column in range(0, len(self.adjacency_matrix[index]) ):
                if(self.adjacency_matrix[index][column] > 0):
                    neighborsList.append(Node(column) )
            return neighborsList
        else:
            return []

    def add_node(self, node):
        if node in self.nodes:
            return False
        else:
            self.nodes.append(node) # add node to nodes list
            for node in self.adjacency_matrix: # adjust length of adjacency_matrix
                node.append(0) # add another empty column to each node
            self.adjacency_matrix.append([0] * len(self.nodes) ) # add an empty row for the new node to adj_matrix list
            return True

    def remove_node(self, node):
        # check if in nodes list
        if node in self.nodes:
            # get row / column index of node
            index = self.nodes.index(node)
            
            #remove node from nodes list
            self.nodes.remove(node)
            #del self.nodes[index]
            
            # remove adjacency_matrix[row] of node
            #self.adjacency_matrix.remove(index)
            del self.adjacency_matrix[index]
            
            # remove adjacency_matrix[column] of node
            for column in self.adjacency_matrix:
                #column.pop(index)
                del column[index]
            return True
        else:
            return False

    def add_edge(self, edge):
        if(edge.from_node in self.nodes and edge.to_node in self.nodes):
            # get weight of edge
            weight = edge.weight
            # find index of from/to node in node list (respectively ;) )
            fromNodeIndex = self.nodes.index(edge.from_node)
            toNodeIndex = self.nodes.index(edge.to_node)
            # set weight to that row/column index
            if(self.adjacency_matrix[fromNodeIndex][toNodeIndex] == weight):
                return False
            else:
                self.adjacency_matrix[fromNodeIndex][toNodeIndex] = weight
            return True
        else:
            return False

    def remove_edge(self, edge):
        if(edge.from_node in self.nodes and edge.to_node in self.nodes):
            # find index of from/to node in node list (respectively ;) )
            fromNodeIndex = self.nodes.index(edge.from_node)
            toNodeIndex = self.nodes.index(edge.to_node)
            # set weight to that row/column index
            if(self.adjacency_matrix[fromNodeIndex][toNodeIndex] == 0):
                return False
            else:
                self.adjacency_matrix[fromNodeIndex][toNodeIndex] = 0
                return True
        else:
            return False

    def get_edge(self, node_1, node_2): # returns edge without checking/comparing weight
        if( (node_1 in self.nodes) and (node_2 in self.nodes) ):
            from_node_index = self.nodes.index(node_1)
            to_node_index = self.nodes.index(node_2)
            weight = self.adjacency_matrix[from_node_index][to_node_index] # index must exist since if-statement checked..
            if(weight > 0):
                return Edge(node_1, node_2, weight) # creates an Edge object just for this, though they don't exists (aren't needed) in this class
            else:
                return None
        else:
            return None
        
    def distance(self, node_1, node_2):
        edge = self.get_edge(node_1, node_2)
        if(edge != None):
            return edge.weight
        else:
            return None

    def __get_node_index(self, node): # I'll implement this if I have time to rewrite
        """helper method to find node index"""
        if(node in self.nodes):
            return self.nodes.index(node)
        else:
            return None

class ObjectOriented(object):
    """ObjectOriented defines the edges and nodes as both list"""
    def __init__(self):
        # implement your own list of edges and nodes
        self.edges = []
        self.nodes = []

    def adjacent(self, node_1, node_2):
        for edge in self.edges:
            if(edge.from_node == node_1 and edge.to_node == node_2): # only checks one way now
                return True
        return False

    def neighbors(self, node):
        nodeNeighbors = []
        for edge in self.edges:
            if(node == edge.from_node):
                nodeNeighbors.append(edge.to_node)
        return nodeNeighbors

    def add_node(self, node):
        if(node in self.nodes):
            return False
        else:
            self.nodes.append(node)
            return True

    def remove_node(self, node): # have to remove edges too
        if(node in self.nodes):
            self.nodes.remove(node)
            for edge in self.edges:
                if(edge.from_node == node or edge.to_node == node):
                    self.edges.remove(edge)
            return True
        else:
            return False

    def add_edge(self, edge):
        if(edge in self.edges):
            return False
        else:
            self.edges.append(edge)
            return True

    def remove_edge(self, edge):
        if(edge in self.edges):
            self.edges.remove(edge)
            return True
        else:
            return False

    def get_edge(self, node_1, node_2): # returns edge without checking/comparing weight
        for edge in self.edges:
            if(edge.from_node == node_1 and edge.to_node == node_2):
                return edge
        return None

    def distance(self, node_1, node_2):
        edge = self.get_edge(node_1, node_2)
        if(edge != None):
            return edge.weight
        else:
            return None # edges value is None... either way
