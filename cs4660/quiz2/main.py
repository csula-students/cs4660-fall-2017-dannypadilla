"""
quiz2!
Use path finding algorithm to find your way through dark dungeon!
Tecchnical detail wise, you will need to find path from node 7f3dc077574c013d98b2de8f735058b4
to f1f131f647621a4be7c71292e79613f9
TODO: implement BFS
TODO: implement Dijkstra utilizing the path with highest effect number
"""

import json
import codecs
import graph
from graph import Edge
import searches
import queue

# http lib import for Python 2 and 3: alternative 4
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

GET_STATE_URL = "http://192.241.218.106:9000/getState"
STATE_TRANSITION_URL = "http://192.241.218.106:9000/state"

def get_path(current_node, distances_d, parents_d):
    path = []
    parent_node = parents_d[current_node]
    while(parent_node != None):
        distance =  distances_d[current_node] - distances_d[parent_node]
        edge = Edge(parent_node, current_node, distance)
        path.append(edge)
        current_node = parent_node # for next loop
        parent_node = parents_d[current_node]
    
    path.reverse()
    return path

def get_edge(from_node_id, to_node_id, edge):
    weight = edge['event']['effect']
    return Edge(from_node_id, to_node_id, weight)

def distance(edge):
    if(edge != type(Edge) ):
        return edge['event']['effect']
    else:
        return edge.weight

def room_print_format(edge):
    from_node_id = edge.from_node
    to_node_id = edge.to_node
    
    from_node = get_state(from_node_id)
    to_node = get_state(to_node_id)
    
    from_node_name = from_node['location']['name']
    to_node_name = to_node['location']['name']
    
    weight = edge.weight
    
    print(from_node_name, "(", from_node_id, ") : ", to_node_name, "(", to_node_id, ") : ", weight )


def get_state(room_id):
    """
    get the room by its id and its neighbor
    """
    body = {'id': room_id}
    return __json_request(GET_STATE_URL, body)

def transition_state(room_id, next_room_id):
    """
    transition from one room to another to see event detail from one room to
    the other.
    You will be able to get the weight of edge between two rooms using this method
    """
    body = {'id': room_id, 'action': next_room_id}
    return __json_request(STATE_TRANSITION_URL, body)

def __json_request(target_url, body):
    """
    private helper method to send JSON request and parse response JSON
    """
    req = Request(target_url)
    req.add_header('Content-Type', 'application/json; charset=utf-8')
    jsondata = json.dumps(body)
    jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes
    req.add_header('Content-Length', len(jsondataasbytes))
    reader = codecs.getreader("utf-8")
    response = json.load(reader(urlopen(req, jsondataasbytes)))
    return response

def bfs(initial_node_id, dest_node_id):
    initial_node = get_state(initial_node_id)
    dest_node = get_state(dest_node_id)
    
    frontier = queue.Queue()
    explored_set = []
    distances = {initial_node_id: 0}
    parents = {initial_node_id: None}
    #dist = 0
    path = []
    
    frontier.put(initial_node)
    
    while(not frontier.empty() ):
        current_node = frontier.get()
        current_node_id = current_node['id']
        
        if(current_node_id == dest_node_id):
            return get_path(current_node_id, distances, parents)
        
        if(current_node_id not in explored_set):
            explored_set.append(current_node_id)
            
        #dist += 1
        for node in get_state(current_node_id)['neighbors']:
            node_id = node['id']
            if(node_id not in explored_set):
                explored_set.append(node_id)
                frontier.put(node)
                event = transition_state(current_node_id, node_id) # get transition state
                effect_distance = event['event']['effect'] # calc distance with trans state
                distances[node_id] = effect_distance
                parents[node_id] = current_node_id
    return False

def dijkstra_search(initial_node_id, dest_node_id):
    initial_node = get_state(initial_node_id)
    dest_node = get_state(dest_node_id)
    
    explored_set = []
    frontier = queue.PriorityQueue()
    distances = {initial_node_id: 0}
    parents = {initial_node_id: None}
    path = []

    frontier.put( (0, initial_node_id ) )

    while(not frontier.empty() ):
        current_node_id = frontier.get()

        if(current_node_id == dest_node_id):
            return get_path(current_node_id, distances, parents)

        if(current_node_id not in explored_set):
            explored_set.append(current_node_id)
            
        for node in get_state(current_node_id)['neighbors']:
            node_id = node['id']
            
            node_dist = transition_state(current_node_id, node_id)['event']['effect']
            alt_dist = distances[current_node_id] + node_dist

            if(node_id not in explored_set): # don't revisit explored rooms
                explored_set.append(node_id)
                if(node_id not in distances or alt_dist > distances[node_id] ):
                    distances[node_id] = alt_dist
                    frontier.put( (alt_dist, node_id ) )
                    parents[node_id] = current_node_id
    return False

if __name__ == "__main__":
    # Your code starts here
    initial_node_id = '7f3dc077574c013d98b2de8f735058b4'
    dest_node_id = 'f1f131f647621a4be7c71292e79613f9'

    bfs_search = bfs(initial_node_id, dest_node_id)
    
    print("* BFS Path")
    hp = 0
    for edge in bfs_search:
        room_print_format(edge)
        hp += edge.weight
    print("Total hp:", hp)

    dijk = dijkstra_search(initial_node_id, dest_node_id)
    print("\n* Dijkstra")
    hp = 0
    for edge in dijk:
        room_print_format(edge)
        hp += edge.weight
    print("Total hp:", hp)
