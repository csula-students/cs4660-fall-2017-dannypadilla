"""
Searches module defines all different search algorithms
"""
import queue
from graph import graph as g

def bfs(graph, initial_node, dest_node):
    """
    Breadth First Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """

    frontier = queue.Queue()
    explored_set = []
    distances = {
        initial_node: 0
    }
    parents = {
        initial_node: None
    }

    frontier.put(initial_node)

    while( not frontier.empty() ):
        current_node = frontier.get() # take node from queue
        
        if(current_node == dest_node): # found path
            return get_path(current_node, distances, parents)
        
        if(current_node not in explored_set):
            explored_set.append(current_node)
        for node in graph.neighbors(current_node):
            if(node not in explored_set):
                explored_set.append(node) # add child to explored set
                frontier.put(node) # add child to queue
                distances[node] = distances[current_node] + graph.distance(current_node, node) # calculate distance
                parents[node] = current_node # assign parent to child
                
    return False # no path was found

def dfs(graph, initial_node, dest_node):
    """
    Depth First Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    # stack
    pass

def dijkstra_search(graph, initial_node, dest_node):
    """
    Dijkstra Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    # priority queue

    frontier = queue.PriorityQueue()
    explored_set = []
    distances = {
        initial_node: 0
    }
    parents = {
        initial_node: None
    }

    frontier.put( (0, initial_node) )

    while( not frontier.empty() ):
        tup_node = frontier.get()
        current_node = tup_node[1] # take node from queue

        if(current_node == dest_node):
            return get_path(current_node, distances, parents)

        for node in graph.neighbors(current_node):
            
            alt_dist = distances[current_node] + graph.distance(current_node, node)
            
            if(node not in distances or alt_dist < distances[node] ):
                #explored_set.append(node)
                distances[node] = alt_dist
                frontier.put( (alt_dist, node) ) # add child to queue
                #distances[node] = distances[current_node] + graph.distance(current_node, node) # calculate distance
                parents[node] = current_node # assign parent to child
                
    return False # no path was found

def a_star_search(graph, initial_node, dest_node):
    """
    A* Search
    uses graph to do search from the initial_node to dest_node
    returns a list of actions going from the initial node to dest_node
    """
    pass

def get_path(current_node, distances_d, parents_d):
    path = []
    parent_node = parents_d[current_node]
    while(parent_node != None):
        distance =  distances_d[current_node] - distances_d[parent_node]
        edge = g.Edge(parent_node, current_node, distance) # should distance be from parent to node OR initial to dest node?
        path.append(edge) # create new EDGE or get from graph?
        current_node = parent_node # for next loop
        parent_node = parents_d[current_node]
    
    path.reverse()
    return path
