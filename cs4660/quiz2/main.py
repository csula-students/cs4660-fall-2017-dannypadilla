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
import searches
import queue

# http lib import for Python 2 and 3: alternative 4
try:
    from urllib.request import urlopen, Request
except ImportError:
    from urllib2 import urlopen, Request

GET_STATE_URL = "http://192.241.218.106:9000/getState"
STATE_TRANSITION_URL = "http://192.241.218.106:9000/state"

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

if __name__ == "__main__":
    # Your code starts here
    initial_node_id = '7f3dc077574c013d98b2de8f735058b4'
    dest_node_id = 'f1f131f647621a4be7c71292e79613f9'

    initial_node = get_state(initial_node_id)
    dest_node = get_state(dest_node_id)

    frontier = queue.Queue()
    explored_set = []
    distances = {initial_node_id: 0}
    parents = {initial_node_id: None}

    frontier.put(initial_node)

    while(not frontier.empty() ):
        current_node = frontier.get()

        if(current_node == dest_node):
            print(get_path(current_node, distances, parents) )
        if(current_node not in explored_set):
            explored_set.append(current_node)
        for node in current_node['neighbors']:
            if(node not in explored_set):
                explored_set.append(node)
                frontier.put(node)
                #trans_state
                #cn_event_effect = event_effect
                distances[node] = distances[current_node['id']
                parents[node] = current_node
    print("No path")


############ TESTING ##############
    room = get_state(initial_node_id)
    room_id = room['id']
    room_name = room['location']['name']
    room_neighbors = room['neighbors']
    
    #print(transition_state(room['id'], room['neighbors'][0]['id']))

    node = transition_state(room['id'], room['neighbors'][0]['id'])
    id = node['id']
    action = node['action']
    event = node['event']
    event_name = event['name']
    event_desc = event['description']
    event_effect = event['effect']
    

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
