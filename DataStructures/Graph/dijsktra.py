from DataStructures.Graph import dijsktra_structure as dijsktra_st
from DataStructures.Map import map_linear_probing as mp
from DataStructures.Priority_queue import priority_queue as pq
from DataStructures.Stack import stack as st
from DataStructures.Graph import diagraph as g
from DataStructures.Graph import edge as e
from DataStructures.List import array_list as al

def dijkstra(my_graph, source):
    
    g_order = g.order(my_graph)
    aux_structure = dijsktra_st.new_dijsktra_structure(source, g_order)

    
    lista_vertices = g.vertices(my_graph)
    for i in range(al.size(lista_vertices)):
        vertex_key = al.get_element(lista_vertices, i)
        mp.put(aux_structure["visited"], vertex_key,
               {"dist_to": float('inf'), "edge_from": None})
        
    mp.put(aux_structure["visited"], source,
           {"dist_to": 0, "edge_from": None})


    pq.insert(aux_structure["pq"], 0, source)

    while not pq.is_empty(aux_structure["pq"]):
        current_vertex = pq.remove(aux_structure["pq"])
        current_dist = dist_to(current_vertex, aux_structure)

        arcos = g.edges_vertex(my_graph, current_vertex)
        for i in range(al.size(arcos)):
            edge = al.get_element(arcos, i)
            neighbor = e.to(edge)
            weight = e.weight(edge)
            new_dist = current_dist + weight

            if new_dist < dist_to(neighbor, aux_structure):
                mp.put(aux_structure["visited"], neighbor,
                       {"dist_to": new_dist, "edge_from": current_vertex})
                if pq.contains(aux_structure["pq"], neighbor):
                    pq.improve_priority(aux_structure["pq"], new_dist, neighbor)
                else:
                    pq.insert(aux_structure["pq"], new_dist, neighbor)
                    
    return aux_structure

def dist_to(key_v, aux_structure):
    
    if not mp.contains(aux_structure["visited"], key_v):
        raise Exception(f"El vértice '{key_v}' no existe")
    return mp.get(aux_structure["visited"], key_v)["dist_to"]

def has_path_to(key_v, aux_structure):
    
    if not mp.contains(aux_structure["visited"], key_v):
        raise Exception(f"El vértice '{key_v}' no existe")
    return mp.get(aux_structure["visited"], key_v)["dist_to"] != float('inf')

def path_to(key_v, aux_structure):
    
    if not has_path_to(key_v, aux_structure):
        return None

    path = st.new_stack()
    current = key_v
    while current is not None:
        st.push(path, current)
        current = mp.get(aux_structure["visited"], current)["edge_from"]

    return path
