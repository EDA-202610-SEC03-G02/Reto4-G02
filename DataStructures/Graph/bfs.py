from DataStructures.Queue import queue as queue
from DataStructures.Stack import stack as st
from DataStructures.Map import map_linear_probing as lp
from DataStructures.Graph import diagraph as dg
from DataStructures.List import array_list as al
from DataStructures.Graph import edge as eli

def bfs(my_graph, source):
    mapa = lp.new_map(num_elements=dg.order(my_graph),load_factor=0.5)
    lp.put(mapa, source, {
        'edge_to': None,
        'dist_to': 0
    })
    return bfs_vertex(my_graph, source, mapa)

def bfs_vertex(my_graph, source, visited_map):
    cola = queue.new_queue()
    queue.enqueue(cola, source)
    
    while not queue.is_empty(cola):
        vertex = queue.dequeue(cola)

        info_actual = lp.get(visited_map, vertex)
        distancia_actual = info_actual['dist_to']
        
        adyacentes = dg.edges_vertex(my_graph, vertex)
        
        for i in range(al.size(adyacentes)):
            adyacente = al.get_element(adyacentes, i)
            
            vecino = eli.to(adyacente)
        
            if not lp.contains(visited_map, vecino):
                lp.put(visited_map, vecino, {
                    'edge_to': vertex,
                    'dist_to': distancia_actual + 1
                })    
                queue.enqueue(cola, vecino)
                
    return visited_map

def has_path_to(key_v, visited_map):
    return lp.contains(visited_map, key_v)

def path_to(key_v, visited_map):
    if not has_path_to(key_v, visited_map):
        return None
    
    path = st.new_stack()
    vertex = key_v

    while vertex is not None:
        st.push(path, vertex)
        info_actual = lp.get(visited_map, vertex)
        vertex = info_actual['edge_to']
    return path