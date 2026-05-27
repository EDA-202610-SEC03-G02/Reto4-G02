from DataStructures.Map import map_linear_probing as mp
from DataStructures.List import array_list as al
from DataStructures.Stack import stack as st
from DataStructures.Graph import diagraph as G
from DataStructures.Graph import edge as e_lib

def dfs(my_graph, source):
    visited_map = mp.new_map(num_elements=G.order(my_graph), load_factor=0.5)

    mp.put(visited_map, source, {
        "marked": True,
        "edge_from": None
    })

    dfs_vertex(my_graph, source, visited_map)
    return visited_map


def dfs_vertex(my_graph, vertex, visited_map):
    arcos = G.edges_vertex(my_graph, vertex)

    for i in range(al.size(arcos)):
        edge = al.get_element(arcos, i)
        
        adj = e_lib.to(edge)

        if not mp.contains(visited_map, adj):
            mp.put(visited_map, adj, {
                "marked": True,
                "edge_from": vertex
            })
            
            dfs_vertex(my_graph, adj, visited_map)

    return visited_map


def has_path_to(key_v, visited_map):
    return mp.contains(visited_map, key_v)


def path_to(key_v, visited_map):
    if not has_path_to(key_v, visited_map):
        return None

    path = st.new_stack()
    actual = key_v

    while actual is not None:
        st.push(path, actual)
        info = mp.get(visited_map, actual)
        
        if info is None:
            break
            
        actual = info["edge_from"]

    return path