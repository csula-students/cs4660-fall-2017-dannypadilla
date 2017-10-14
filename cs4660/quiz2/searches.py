import queue
import graph

def bfs(graph, initial_node, dest_node):
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

def dijkstra_search(graph, initial_node, dest_node):
    frontier = queue.PriorityQueue()
    explored_set = []
    distances = {
        initial_node: 0
    }
    parents = {
        initial_node: None
    }

    frontier.put((initial_node, distances[initial_node]) )

    while( not frontier.empty() ):
        current_node = frontier.get() # take node from queue
        
        for node in graph.neighbors(current_node):
            alt = distance[current_node] + graph.distance(current_node, node)
            if(alt < distance[node]):
                distance[node] = alt
                frontier.put(node) # add child to queue
                distances[node] = distances[current_node] + graph.distance(current_node, node) # calculate distance
                parents[node] = current_node # assign parent to child
                
    return False # no path was found

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
