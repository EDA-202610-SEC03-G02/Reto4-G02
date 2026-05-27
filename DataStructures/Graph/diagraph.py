from DataStructures.Map import map_linear_probing as mp
from DataStructures.Graph import vertex as v  
from DataStructures.Graph import edge as e

DEFAULT_LOAD_FACTOR = 0.5
DEFAULT_PRIME = 109345121

def new_graph(order):
    grafo = {
        'vertices' :mp.new_map(num_elements=order, load_factor=DEFAULT_LOAD_FACTOR, prime=DEFAULT_PRIME),
        'num_edges' : 0
    }
    return grafo

def insert_vertex(my_graph, key_u, info_u):
   
    nuevo_vertice = v.new_vertex(key_u, info_u)
    
    mp.put(my_graph['vertices'], key_u, nuevo_vertice)
    
    return my_graph

def add_edge(my_graph, key_u, key_v, weight=1.0):
    
    vertice_u = mp.get(my_graph['vertices'], key_u)
    vertice_v = mp.get(my_graph['vertices'], key_v)
    
    if vertice_u is None:
        raise Exception(f"El vértice '{key_u}' no existe en el grafo")
    if vertice_v is None:
        raise Exception(f"El vértice '{key_v}' no existe en el grafo")

    if v.get_edge(vertice_u, key_v) is None:
        v.add_adjacent(vertice_u, key_v, weight)
        my_graph['num_edges'] += 1
    else:
        v.add_adjacent(vertice_u, key_v, weight) 

    return my_graph

def contains_vertex(my_graph, key_u):
    return mp.contains(my_graph['vertices'], key_u)

def order(my_graph):
    return mp.size(my_graph['vertices'])

def size(my_graph):
    return my_graph['num_edges']

def degree(my_graph, key_u):
    vertice_u = mp.get(my_graph['vertices'], key_u)
    
    if vertice_u is None:
        raise Exception("El vertice no existe")
    
    return v.degree(vertice_u)

def adjacents(my_graph, key_u):
    vertice_u = mp.get(my_graph['vertices'], key_u)
    
    if vertice_u is None:
        raise Exception("El vertice no existe")
    
    return v.get_adjacents(vertice_u)

def vertices(my_graph):
    return mp.key_set(my_graph['vertices'])

def edges_vertex(my_graph, key_u):
    vertice_u = mp.get(my_graph['vertices'], key_u)
    
    if vertice_u is None:
        raise Exception("El vertice no existe")
    
    adyacentes = v.get_adjacents(vertice_u)
    return mp.value_set(adyacentes)



def get_vertex(my_graph, key_u):
    vertice_u = mp.get(my_graph['vertices'], key_u)
    
    if vertice_u is None:
        return None
    
    return vertice_u

def update_vertex_info(my_graph, key_u, new_info_u):
    vertice_u = mp.get(my_graph['vertices'], key_u)
    
    if vertice_u is not None:
        v.set_value(vertice_u, new_info_u)
    
    return my_graph

def get_vertex_information(my_graph, key_u):
    vertice_u = mp.get(my_graph["vertices"], key_u)

    if vertice_u is None:
        raise Exception("El vertice no existe")

    return v.get_value(vertice_u)


    