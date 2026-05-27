import time 
import math
import csv
import os
from datetime import datetime
from DataStructures.Map import map_linear_probing as mp
from DataStructures.List import array_list as al
from DataStructures.Graph import diagraph as gr
from DataStructures.Graph import bfs as bfs
from DataStructures.Graph import edge as edge

data_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '/Data/Data/'


def new_logic():
    """
    Crea el catalogo para almacenar las estructuras de datos
    """
    #TODO: Llama a las funciónes de creación de las estructuras de datos
    analyzer = {}
    capacity = 1000000 # revisar el numero
    load_factor = 0.5
    analyzer["vertices_map"] = mp.new_map(capacity, load_factor) #HECHO
    analyzer["mmsi_records_map"] = mp.new_map(capacity, load_factor)
    analyzer["edge_info_map"] = mp.new_map(capacity, load_factor)
    analyzer["g_distance"] = gr.new_graph(capacity)  
    analyzer["g_time"] = gr.new_graph(capacity) 
    analyzer["total_records"] = 0
    analyzer["total_vessels"] = 0
    analyzer["creation_orden"] = al.new_list()

    return analyzer


# Funciones para la carga de datos
def new_cluster(dest_cluster):
    cluster = {
        "id": dest_cluster,

        "lat_sum": 0.0,
        "lon_sum": 0.0,
        "sog_sum": 0.0,
        "length_sum": 0.0,
        "width_sum": 0.0,
        "draft_sum": 0.0,

        "records_count": 0,

        "mmsi_list": al.new_list(),
        "mmsi_set": mp.new_map(100, 0.5),
        "vessel_names": al.new_list(),
        "vessel_names_set": mp.new_map(100, 0.5),
        "vessel_types": al.new_list(),
        "vessel_types_set": mp.new_map(100, 0.5),
        "cargo_types": al.new_list(),
        "cargo_types_set": mp.new_map(100, 0.5),
        "speed_categories": al.new_list(),
        "speed_categories_set": mp.new_map(100, 0.5),
        "records": al.new_list(),

        "lat": None,
        "lon": None,
        "avg_sog": None,
        "avg_length": None,
        "avg_width": None,
        "avg_draft": None
    }
    return cluster

def compare_elements(element_a, element_b):
    if str(element_a).strip() == str(element_b).strip():
        return 0
    return -1

def add_record_to_cluster(cluster, record):
    cluster["lat_sum"] += float(record["LAT"])
    cluster["lon_sum"] += float(record["LON"])
    cluster["sog_sum"] += float(record["SOG"])
    
    if record["LENGTH"] != "":
        cluster["length_sum"] += float(record["LENGTH"]) 
    if record["WIDTH"] != "":
        cluster["width_sum"] += float(record["WIDTH"])
    if record["DRAFT"] != "":
        cluster["draft_sum"] += float(record["DRAFT"])
    
    cluster["records_count"] += 1

    al.add_last(cluster["records"], record)
    
    mmsi = record["MMSI"]
    if not mp.contains(cluster["mmsi_set"], mmsi):
        mp.put(cluster["mmsi_set"], mmsi, True)
        al.add_last(cluster["mmsi_list"], mmsi)
        
    vessel_name = record["VESSELNAME"]
    if not mp.contains(cluster["vessel_names_set"], vessel_name):
        mp.put(cluster["vessel_names_set"], vessel_name, True)
        al.add_last(cluster["vessel_names"], vessel_name)
    
    vessel_type = record["VESSELTYPE"]
    if not mp.contains(cluster["vessel_types_set"], vessel_type):
        mp.put(cluster["vessel_types_set"], vessel_type, True)
        al.add_last(cluster["vessel_types"], vessel_type)
    
    cargo_type = record["CARGO"]
    if not mp.contains(cluster["cargo_types_set"], cargo_type):
        mp.put(cluster["cargo_types_set"], cargo_type, True)
        al.add_last(cluster["cargo_types"], cargo_type)
    
    speed_category = record["SPEED_CATEGORY"]
    if not mp.contains(cluster["speed_categories_set"], speed_category):
        mp.put(cluster["speed_categories_set"], speed_category, True)
        al.add_last(cluster["speed_categories"], speed_category)

def calculate_cluster_averages(cluster):
    if cluster["records_count"] > 0:
        cluster["lat"] = cluster["lat_sum"] / cluster["records_count"]
        cluster["lon"] = cluster["lon_sum"] / cluster["records_count"]
        cluster["avg_sog"] = round(cluster["sog_sum"] / cluster["records_count"], 2)
        cluster["avg_length"] = round(cluster["length_sum"] / cluster["records_count"], 2)
        cluster["avg_width"] = round(cluster["width_sum"] / cluster["records_count"], 2)
        cluster["avg_draft"] = round(cluster["draft_sum"] / cluster["records_count"], 2)

def add_record_to_mmsi_map(catalog, record):
    
    mmsi = record["MMSI"]
    records_list = mp.get(catalog["mmsi_records_map"], mmsi)
    
    if records_list is None:
        records_list = al.new_list()
    mp.put(catalog["mmsi_records_map"], mmsi, records_list)
    
    al.add_last(records_list, record)

def new_edge_info(source, target, distance):
    
    edge_info = {
        "source": source,
        "target": target,
        "trips_count": 0,
        "distance": distance,
        "times" : al.new_list(),
        "trip_mmsi_list": al.new_list(),
        "trip_speed_categories": al.new_list(),
        "avg_time": None
    }
    return edge_info

def add_trip_to_edge_info(edge_info, trip_time, mmsi, speed_category):
    edge_info["trips_count"] += 1
    al.add_last(edge_info["times"], trip_time)
    al.add_last(edge_info["trip_mmsi_list"], mmsi)
    al.add_last(edge_info["trip_speed_categories"], speed_category)

def build_edges_info_map(catalog):
    mmsi_map = catalog["mmsi_records_map"]
    mmsi_keys = mp.key_set(mmsi_map)
    total_keys = al.size(mmsi_keys)
    
    for i in range(total_keys):
        mmsi = al.get_element(mmsi_keys, i)
        sort_records = mp.get(mmsi_map, mmsi)
        
        if sort_records is not None:
            total_records = al.size(sort_records)    
        for j in range(total_records-1):
            record_a = al.get_element(sort_records, j)
            record_b = al.get_element(sort_records, j+1)
            
            source = record_a["DEST_CLUSTER"].strip()
            target = record_b["DEST_CLUSTER"].strip()
            
            if source != target:
                edge_id = source + "-" + target
                trip_time = calculate_time_difference(record_a["BASEDATETIME"], record_b["BASEDATETIME"])
                speed_category = record_b["SPEED_CATEGORY"]
                
                edge_info = mp.get(catalog["edge_info_map"], edge_id)
                
                if edge_info is None:
                    source_vertex = mp.get(catalog["vertices_map"], source)
                    target_vertex = mp.get(catalog["vertices_map"], target)
                  
                    if source_vertex is not None and target_vertex is not None:
                        distance = haversine_distance(source_vertex["lat"], source_vertex["lon"], target_vertex["lat"], target_vertex["lon"])        
                        edge_info = new_edge_info(source, target, distance)
                        mp.put(catalog["edge_info_map"], edge_id, edge_info)
                    
                if edge_info is not None:
                    add_trip_to_edge_info(edge_info, trip_time, mmsi, speed_category)
                
def haversine_distance(lat1, lon1, lat2, lon2):
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    radius_earth_km = 6371
    distance = radius_earth_km * c
    return distance

def calculate_time_difference(datetime_a, datetime_b):
    date_format = "%Y-%m-%d %H:%M:%S"
    dt_a = datetime.strptime(datetime_a, date_format)
    dt_b = datetime.strptime(datetime_b, date_format)
    time_dif = dt_b - dt_a
    return time_dif.total_seconds()

def calculate_edges_avg_time(catalog):
    edge_info_map = catalog["edge_info_map"]
    edge_keys = mp.key_set(edge_info_map)
    total_edges = al.size(edge_keys)
    
    for i in range(total_edges):
        edge_id = al.get_element(edge_keys, i)
        edge_info = mp.get(edge_info_map, edge_id)
        
        if edge_info is not None:
            times = edge_info["times"]
            total_times = al.size(times)
        
            if total_times > 0:
                total = 0
                for j in range(total_times):
                    total += al.get_element(times, j)
                avg = total / total_times
                edge_info["avg_time"] = round(avg, 2)
        
def build_graphs(catalog):
    vertices_map = catalog["vertices_map"]
    vertices_keys = mp.key_set(vertices_map)
    total_vertices = al.size(vertices_keys)
    
    for i in range(total_vertices):
        vertex_id = al.get_element(vertices_keys, i)
        vertex_info = mp.get(vertices_map, vertex_id)
        
        gr.insert_vertex(catalog["g_distance"], vertex_id, vertex_info)
        gr.insert_vertex(catalog["g_time"], vertex_id, vertex_info)
        
    edge_info_map = catalog["edge_info_map"]
    edge_keys = mp.key_set(edge_info_map)
    total_edges = al.size(edge_keys)
    
    for i in range(total_edges):
        edge_id = al.get_element(edge_keys, i)
        edge_info = mp.get(edge_info_map, edge_id)
        
        if edge_info is not None and edge_info["avg_time"] is not None:
            source = edge_info["source"]
            target = edge_info["target"]
            distance = edge_info["distance"]
            avg_time = edge_info["avg_time"]
            gr.add_edge(catalog["g_distance"], source, target, distance)
            gr.add_edge(catalog["g_time"], source, target, avg_time)

def load_data(catalog, filename):
    """
    Carga los datos del reto
    """
    start_time = get_time()
    computer_file = data_dir + filename
    file = open(computer_file, encoding="utf-8")
    input_file = csv.DictReader(file)
    
    for record in input_file:
        cluster_id = record["DEST_CLUSTER"].strip()
        cluster = mp.get(catalog["vertices_map"], cluster_id)
        
        if cluster is None:
            cluster = new_cluster(cluster_id)
            mp.put(catalog["vertices_map"], cluster_id, cluster)
            al.add_last(catalog["creation_orden"], cluster_id)
        
        add_record_to_cluster(cluster, record)
        add_record_to_mmsi_map(catalog, record)
        catalog["total_records"] += 1
    
    file.close()
    
    vertex_keys = mp.key_set(catalog["vertices_map"])
    for i in range(al.size(vertex_keys)):
        vertex_id = al.get_element(vertex_keys, i)
        cluster = mp.get(catalog["vertices_map"], vertex_id)
        calculate_cluster_averages(cluster)
    
    build_edges_info_map(catalog)
    calculate_edges_avg_time(catalog)
    build_graphs(catalog)
    
    catalog["total_vessels"] = al.size(mp.key_set(catalog["mmsi_records_map"]))
    
    total_vertices = gr.order(catalog["g_distance"])
    total_arcos = gr.size(catalog["g_distance"])
    
    primeros_5 = []
    ultimos_5 = []
    
    lista_ordenada = catalog["creation_orden"]
    total = al.size(lista_ordenada)
    
    for i in range(5):
        vertex_id = al.get_element(lista_ordenada, i)
        vertex_info = mp.get(catalog["vertices_map"], vertex_id)
        primeros_5.append(vertex_info)
    
    for i in range(total - 5, total):
        vertex_id = al.get_element(lista_ordenada, i)
        vertex_info = mp.get(catalog["vertices_map"], vertex_id)
        ultimos_5.append(vertex_info)
    
    end_time = get_time()
    tiempo = delta_time(start_time, end_time)
    
    return  {
        "tiempo": tiempo,
        "total_vessels": catalog["total_vessels"],
        "total_records": catalog["total_records"],
        "total_vertices": total_vertices,
        "total_arcos": total_arcos,
        "primeros_5": primeros_5,
        "ultimos_5": ultimos_5
    }
# Funciones de consulta sobre el catálogo


def req_1(catalog):
    """
    Retorna el resultado del requerimiento 1
    """
    # TODO: Modificar el requerimiento 1
    pass


def req_2(catalog):
    """
    Retorna el resultado del requerimiento 2
    """
    # TODO: Modificar el requerimiento 2
    pass


def req_3(catalog, n):
    """
    Retorna el resultado del requerimiento 3
    """
    # TODO: Modificar el requerimiento 3
    edge_info_map = catalog["edge_info_map"]
    arcos_lista = mp.value_set(edge_info_map)
    
    al.merge_sort(arcos_lista, comparar_arcos_req3)
    
    resultado = al.new_list()
    if al.size(arcos_lista) > n:
        limite = n
    else:
        limite = al.size(arcos_lista)
    
        
    for i in range(limite):
        edge_info = al.get_element(arcos_lista, i)
        
        distancia = edge_info["distance"]
        tiempo = edge_info["avg_time"]
    
        if distancia is not None:
            dist_final = distancia
        else:
            dist_final = "Unknown"
        if tiempo is not None:
            tiempo_final = tiempo
        else:
            tiempo_final = "Unknown"
            
        info = {
            "origen": edge_info["source"],
            "destino": edge_info["target"],
            "cantidad_viajes": edge_info["trips_count"],
            "distancia": dist_final,
            "tiempo_promedio": tiempo_final
        }
        
        al.add_last(resultado, info)
    
    return resultado

def comparar_arcos_req3(arco_a, arco_b):
    if arco_a["trips_count"] != arco_b["trips_count"]:
        return arco_a["trips_count"] > arco_b["trips_count"]
        
    if arco_a["source"] != arco_b["source"]:
        return arco_a["source"] < arco_b["source"]
        
    return arco_a["target"] < arco_b["target"]

def req_4(catalog):
    """
    Retorna el resultado del requerimiento 4
    """
    # TODO: Modificar el requerimiento 4
    pass


def req_5(catalog):
    """
    Retorna el resultado del requerimiento 5
    """
    # TODO: Modificar el requerimiento 5
    pass

def req_6(catalog):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    grafo_dirigido = catalog["g_distance"]
    vertices_lista = gr.vertices(grafo_dirigido)
    total_vertices = gr.order(grafo_dirigido)
    
    if total_vertices == 0:
        return al.new_list()
    
    g_nodir = crear_grafo_no_dirigido(grafo_dirigido, vertices_lista, total_vertices, catalog)

    visited_map = mp.new_map(total_vertices*2, 0.5)
    subrarcos_list = al.new_list()
    
    for i in range(total_vertices):
        raiz_id = al.get_element(vertices_lista, i)
        
        if not mp.contains(visited_map, raiz_id):
            mapa_sub_actual = mp.new_map(total_vertices*2, 0.5)
            mp.put(mapa_sub_actual, raiz_id, {"edge_to": None, "dist_to": 0})
            bfs.bfs_vertex(g_nodir, raiz_id, mapa_sub_actual)
            
            subred_data = procesar_subred(vertices_lista, total_vertices, mapa_sub_actual, visited_map, catalog)
            al.add_last(subrarcos_list, subred_data)
            
    al.merge_sort(subrarcos_list,comparar_subredes)
    resultado = al.new_list()
    total_global = al.size(subrarcos_list)
    if total_global > 5:
        limite = 5
    else:
        limite = total_global
        
    for i in range(limite):
        subred = al.get_element(subrarcos_list, i)
        info_subred = {
            "subred_id": i+1,
            "total_subred": total_global,
            "total_zonas": subred["total_zonas"],
            "zonas_ids": subred["nodos"],
            "total_viajes": subred["total_viajes"],
            "velocidad_promedio": subred["velocidad_promedio"]
        }
        al.add_last(resultado, info_subred)
    
    return resultado

def comparar_ids_ascendente(id_a, id_b):
    return int(id_a) < int(id_b)

def comparar_subredes(sub_a, sub_b):
    if sub_a["total_zonas"] != sub_b["total_zonas"]:
        return sub_a["total_zonas"] > sub_b["total_zonas"]
    return sub_a["min_vertex_id"] < sub_b["min_vertex_id"]
                
def crear_grafo_no_dirigido(grafo_dirigido, vertices, total_v, catalog):
    grafo_nodir = gr.new_graph(total_v)
    
    for i in range(total_v):
        vertex_id = al.get_element(vertices, i)
        vertex_info = mp.get(catalog["vertices_map"], vertex_id)
        gr.insert_vertex(grafo_nodir, vertex_id, vertex_info)
    
    for i in range(total_v):
        vertex_id = al.get_element(vertices, i)
        adyacentes = gr.edges_vertex(grafo_dirigido, vertex_id)
        
        for j in range(al.size(adyacentes)):
            arco = al.get_element(adyacentes, j)
            vecino_id = edge.to(arco)
            
            if vertex_id != vecino_id:
                arcos_regreso = gr.edges_vertex(grafo_dirigido, vecino_id)
                existe_arco_regreso = False
                
                for k in range(al.size(arcos_regreso)):
                    arco_regreso = al.get_element(arcos_regreso, k)
                    vecino_regreso_id = edge.to(arco_regreso)
                    
                    if vecino_regreso_id == vertex_id:
                        existe_arco_regreso = True
                        break
                    
                if existe_arco_regreso:
                    gr.add_edge(grafo_nodir, vertex_id, vecino_id, 1.0)
                    gr.add_edge(grafo_nodir, vecino_id, vertex_id, 1.0)
    return grafo_nodir

def procesar_subred(vertices_lista, total_vertices, mapa_subred, visited_map, catalog):
    nodos_subred = al.new_list()
    total_viajes = 0
    suma_velocidades = 0.0
    
    viaje_valido = True
    velocidad_valida = True
    
    for i in range(total_vertices):
        vertice_id = al.get_element(vertices_lista, i)
        if mp.contains(mapa_subred, vertice_id):
            mp.put(visited_map, vertice_id, True)
            al.add_last(nodos_subred, vertice_id)
            vertice_info = mp.get(catalog["vertices_map"], vertice_id)
            if vertice_info:
                if "records_count" in vertice_info and vertice_info["records_count"] is not None:
                    total_viajes += vertice_info["records_count"]
                else:
                    viaje_valido = False
                if "avg_sog" in vertice_info and vertice_info["avg_sog"] is not None:
                    suma_velocidades += vertice_info["avg_sog"]
                else:
                    velocidad_valida = False
            else:
                viaje_valido = False
                velocidad_valida = False
    
    al.merge_sort(nodos_subred, comparar_ids_ascendente)
    total_zonas = al.size(nodos_subred)
        
    if total_zonas > 0 and velocidad_valida:
        velocidad_promedio = round(suma_velocidades / total_zonas, 2)
    else:
        velocidad_promedio = "Unknown"
        
    if not viaje_valido:
        total_viajes = "Unknown"
        
    if total_zonas > 0:
        min_vertex_id = int(al.get_element(nodos_subred, 0))
    else:
        min_vertex_id = float('inf')
        
    return {
        "total_zonas": total_zonas,
        "nodos": nodos_subred,
        "total_viajes": total_viajes,
        "velocidad_promedio": velocidad_promedio,
        "min_vertex_id": min_vertex_id
    }
    
# Funciones para medir tiempos de ejecucion

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed
